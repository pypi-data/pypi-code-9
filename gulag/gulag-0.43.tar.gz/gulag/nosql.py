# coding=utf-8

from datetime import datetime
import json
import re
import time
import traceback

from bson.objectid import ObjectId
from pymongo.database import Database, Collection
from pymongo import ReadPreference, MongoClient, DESCENDING, ASCENDING
from pymongo.errors import ConfigurationError, OperationFailure,  AutoReconnect


from gulag import exception


__all__ = ['MongoModel', 'ObjectId', 'IS_TEST', "Collection", 'conf', "DESCENDING", "ASCENDING"]

UTC = datetime.utcnow


class Config(object):
    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self.__dict__[key] = getattr(obj, key)

        if hasattr(self, "MONGO_METRICS"):
            if "DB_NAME" not in self.MONGO_METRICS:
                raise exception.ConfigError("MONGO_METRICS must be a dictionary with DB_NAME & COL_NAME string members")
        else:
            self.MONGO_METRICS = None


conf = Config()


def tidy_cursor(doc_iter):
    """
    N.B. CURSOR ONLY Format Mongo documents to permit simpler jsonification
    """
    for idx, doc in enumerate(doc_iter):
        if "_id" in doc:
            doc["rec_id"] = str(doc.pop("_id"))
        doc["idx"] = idx
        yield doc

# Determine whether we are running in test mode, by looking in call stack
_stck = [i[0] for _i in traceback.extract_stack() if 'tests' in _i[0]]
IS_TEST = len(_stck) > 0

NOSQL_NET_TIMEOUT = 30 * 1000
NUM_MONGO_AUTO_CONNECT_RETRY = 5

CON =  {}  # MongoDB connections

def get_con(host):
    if not host:
        assert (
            hasattr(conf, "MONGO_URL")
            and len(conf.MONGO_URL)
        ), 'MONGO_URL not configured'
        host = conf.MONGO_URL

    try:
        if host not in CON:
            CON[host] = MongoClient(
                host=host,
            )

    except ConfigurationError as exc:
        err =  "Exc: %s, host: %s" % (
            exc, host,
        )
        raise ConfigurationError(err)

    except AutoReconnect as exc:
        raise  AutoReconnect("%s (%s)" % (
            exc, "Check that mongodb service has been started")
        )
    return CON[host]


class GridFile(object):
    def __init__(self, col_name=None, host=None):
        assert self.db_name, "Specify db_name"

        self.db_name = 'test_%s' % self.db_name  if IS_TEST else self.db_name
        if col_name is not None:
            self.col_name = col_name

        self._con = get_con(host=host)
        self._db = self._con[self.db_name]
        if conf.USE_MONGODB_AUTH:
            self._db.authenticate(*conf.MONGO_SECRET)
        self._db.read_preference = ReadPreference.SECONDARY
        self.gfs = GridFS(database=self._db, collection=self.col_name)

    def __getattr__(self, attr):
        """
        Pass collection-level operations to contained collection
        """
        assert self.col_name != "empty", "Invalid operation on abstract model"
        if attr in [
            "find_one", "insert", "update", "delete", "find", "find_and_modify", "create_index", "index_information"
            ]:
            return Functor(profile_func=getattr(self.gfs, attr))

        else:
            raise AttributeError("Unkown attribute: %s" % attr)

    def remove_all(self):
        self._db.drop_collection(self.col_name + ".files")
        self._db.drop_collection(self.col_name + ".chunks")

    def delete(self, _id):
        self.gfs.delete(file_id=ObjectId(_id))

    def get(self, _id):
        doc = self.gfs.get(file_id=ObjectId(_id))
        doc.rid = doc._id
        return doc

    def get_last_version(self, filename):
        doc = self.gfs.get_last_version(filename=filename)
        doc.rid = doc._id
        return doc

    def get_io(self, _id):
        grid_out = self.get(_id)
        return grid_out.read()

    def get_b64(self, _id):
        dta = self.get_io(_id)
        return b64encode(dta)

    def b64(self, grid_out):
        dta = grid_out.read()
        return b64encode(dta)

    def make_temp_file(self, _id, delete=False):
        """
        Write binary data to a temporary file
        """
        dta = self.get_io(_id)
        tempf = NamedTemporaryFile(delete=delete)
        tempf.write(dta)
        tempf.close()
        path = tempf.name
        return path

    def make_empty_temp_file(self, delete=False):
        tempf = NamedTemporaryFile(delete=delete)
        path = tempf.name
        tempf.close()
        return path

    def recent(self):
        return self.gfs._GridFS__files.find().sort('uploadDate')

    def upload(self, file_store, ref=None, content_type=None, **kwargs):
        assert content_type, "Not willing to guess mimetype"

        if issubclass(file_store.__class__, basestring):
            if not os.path.exists(file_store):
                raise exception.PathNotFound(file_store)

            file_store = file(file_store, "rb")

        if ref is None:
            ref = ObjectId()

        buf = file_store.read()

        file_store.seek(0)
        _id = self.gfs.put(
            filename=ref,
            content_type=content_type,
            data=buf,
            **kwargs
        )
        return _id


class Functor(object):
    """
    Every collection-level operation thru here
    AutoReconnect handling support provided, capability of logging mongo operation
    """
    def __init__(self, profile_func):
        self.mongo_func = profile_func
        (self.num_auto_connect_retry, self.auto_retry_delay_seconds) = 0, 0.2
        if conf.MONGO_METRICS:
            met_col_name=conf.MONGO_METRICS.get("COL_NAME", "mongo_detail")
            met_db_name=conf.MONGO_METRICS.get("DB_NAME")
            metrics_con = get_con(host=None)  # settings.MONGO_URL
            self.met_db = metrics_con[met_db_name]
            self.met_col = self.met_db[met_col_name]

    def ant_detail(self, dur_ms, data):
        """
        Output analytics detail
        """
        if dur_ms > conf.MONGO_METRICS["LIMIT_MS"]:
            self.met_col.insert({
                "utc": UTC(),
                "func": self.mongo_func.__name__,
                "dur_ms": dur_ms,
                "data": json.dumps(data),
            })

    def __call__(self, *args, **kwargs):
        """
        Operation call
        """
        while True:
            try:
                if conf.MONGO_METRICS:
                    start_time = time.time()
                _res = self.mongo_func(*args, **kwargs)
                if conf.MONGO_METRICS:
                    dur_ms = (time.time() - start_time) * 1000.0
                    data = kwargs
                    data["args"] = args
                    self.ant_detail(dur_ms=dur_ms, data=data)
                return _res

            except AutoReconnect:
                self.num_auto_connect_retry += 1
                if self.num_auto_connect_retry > NUM_MONGO_AUTO_CONNECT_RETRY:
                    raise  exception.MongoConnectionLost(
                        "Failed mongodb autoconnect, after %s attempts" % NUM_MONGO_AUTO_CONNECT_RETRY
                    )
                time.sleep(self.auto_retry_delay_seconds)
                self.auto_retry_delay_seconds *= 2


class MongoModel(object):
    """
    Model abstract class
    If capped collection required, specify `capped_size` (kilobytes) class parameter
    """
    (host, db_name, col_name) = None, None, None
    (db_name, max_records, capped_size) = None, None, None

    def __init__(self, col_name=None, db_name=None, host=None, **kwargs):
        assert hasattr(conf, "MONGO_URL"), "setting.py must contain MONGO_URL"
        if db_name:
            self.db_name = db_name

        # Prefix test-environment databases with 'test_'
        self.db_name = 'test_%s' % self.db_name  if IS_TEST else self.db_name

        if host:
            self.host = host

        if col_name:
            self.col_name = col_name

        if not self.db_name:
            raise ConfigurationError("Cannot proceed without model attribute: db_name")

        if self.col_name is None:
            self.col_name = from_camel(self.__class__.__name__)

        # Limit test capped collection size
        if IS_TEST and self.capped_size:
            self.capped_size = 1 * 1024 * 1024

        if self.capped_size:
            kwargs["capped"] = True
            kwargs["size"] = self.capped_size

        if self.max_records:
            kwargs["max"] = self.max_records

        self._con = get_con(host=self.host)
        self.set_db(db_name=self.db_name)

        if hasattr(self, 'index') and not IS_TEST:
            if not hasattr(self.index, "__iter__"):
                raise Exception("Bad index specification: %s, specify a list of index tuples" % index)

            if self.index and not hasattr(self.index[0], '__iter__'):  # Single index
                self.index = [self.index]

            for _x in self.index:
                if type(_x) != tuple:
                    raise exception.ConfigError("Non tuple index specification: %s" % _x)

            order = lambda xx: (xx[1:], DESCENDING) if xx[0] == '-' else (xx, ASCENDING)
            index_info = self._col.index_information()

            for idx in self.index:
                self.create_index([order(xx) for xx in idx], background=True)


        #self._db.read_preference = ReadPreference.PRIMARY

        # Indexing specifications, eg.
        # [
        #    ("field", "-field2"),
        # ]

    def set_db(self, db_name):
        """
        Separate DB initialisation: to enable database switching
        """
        self.db_name = db_name
        self._db = self._con[self.db_name]
        self._col = self._db[self.col_name]

    def disconnect(self):
        self._con.disconnect()

    def get_collection_stats(self):
        """
        Get stats in kilobytes
        """
        return self._db.command('collstats', self.col_name, scale=1024)

    def drop_database(self):
        self._con.drop_database(self._db)

    def repair_database(self):
        """
        Repair database will recover unused disk space
        Run this from a cron tab
        """
        self._db.command("repairDatabase")

    def __getattr__(self, attr):
        """
        Pass collection level operations to contained collection
        """
        assert self.col_name != "empty", "Invalid operation on abstract model"
        if attr in [
            "find_one", "insert", "update", "remove", "find", "find_and_modify", "drop_indexes", "create_index", "index_information"
            ]:
            return Functor(profile_func=getattr(self._col, attr))

        elif attr not in self.__dict__:
            raise AttributeError("Unkown attribute: %s" % attr)


    def drop_collection(self, col_name):
        self._db.drop_collection(col_name)

    def exists(self):
        fn = Functor(profile_func=self._db.collection_names)
        does_exist = self.col_name in fn()
        return does_exist


    def get_by_id(self, _id, field="_id", **extra):
        """
        Retrieve document by object id
        """
        crit = {
            field: ObjectId(_id) if not isinstance(_id, ObjectId) else _id
        }
        if extra:
            crit.update(extra)
        return self.find_one(crit)


def from_camel(name):
    """
    ThisIsCamelCase ==> this_is_camel_case (Django naming standard)
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name.replace("_", ""))
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
