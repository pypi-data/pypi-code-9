# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- Data loader from YAML
# :Creato:    mer 10 feb 2010 14:35:05 CET
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

"""Load new instances in the database, or update/delete existing ones, given a data structure
represented by a YAML stream, as the following::

    - entity: gam.model.Fascicolo
      key: descrizione
      # no data, just "declare" the entity

    - entity: gam.model.TipologiaFornitore
      key: tipologiafornitore
      data:
        - &tf_onesto
          tipologiafornitore: Test fornitori onesti

    - entity: gam.model.ClienteFornitore
      key: descrizione
      data:
        - descrizione: Test altro fornitore onesto
          tipologiafornitore: *tf_onesto
          partitaiva: 01234567890
        - &cf_lele
          codicefiscale: GFSMNL68C18H612V
          descrizione: Dipendente A

    - entity: gam.model.Dipendente
      key: codicefiscale
      data:
        - &lele
          codicefiscale: GFSMNL68C18H612V
          nome: Emanuele
          cognome: Gaifas
          clientefornitore: *cf_lele
          foto: !File {path: ../img/lele.jpg}

    - entity: gam.model.Attrezzature
      key: descrizione
      data:
        - &macchina
          descrizione: Fiat 500

    - entity: gam.model.Prestiti
      key:
        - dipendente
        - attrezzatura
      data:
        - dipendente: *lele
        - attrezzatura: *macchina

The ``key`` entry may be either a single attribute name or a list of them, not necessarily
corresponding to the primary key of the entity. To handle the simplest case of structured
values (for example, when a field is backed by a PostgreSQL HSTORE), the key attribute name may
be in the form ``name->slot``::

    - entity: model.Product
      key: description->en
      data:
        - &cage
          description:
            en: "Roadrunner cage"
            it: "Gabbia per struzzi"

With the option ``--save-new-instances`` newly created instances will be written (actually
added) to the given file in YAML format, so that at some point they can be deleted using the
option ``--delete`` on that file. Ideally

::

  dbloady -u postgresql://localhost/test -s new.yaml fixture.yaml
  dbloady -u postgresql://localhost/test -D new.yaml

should remove fixture's traces from the database, if it contains only new data.
"""

from logging import getLogger
from os.path import abspath, dirname, exists, join, normpath
import sys

import yaml


logger = getLogger(__name__)

if sys.version_info.major >= 3:
    basestring = str


class File(yaml.YAMLObject):
    """Facility to read the content of an external file.

    A field may be loaded from an external file, given its pathname
    which is interpreted as relative to the position of the YAML file
    currently loading::

        - entity: cpi.models.Document
          key: filename
          data:
            - filename: image.gif
              content: !File {path: ../image.gif}
    """

    yaml_tag = u'!File'

    basedir = None

    def __init__(self, path):
        self.path = path

    def read(self):
        fullpath = normpath(join(self.basedir, self.path))
        return open(fullpath).read()


class Entity(object):
    """Model instances factory."""

    def __init__(self, model, key, data=None, delete=False):
        self.model = resolve_class_name(model)
        if isinstance(key, basestring):
            key = [key]
        self.key = key
        if isinstance(data, dict):
            data = [data]
        self.data = data
        self.delete = delete

    def __repr__(self):
        return "%s(model=%r, key=%r)" % (
            self.__class__.__name__,
            self.model, self.key)

    def __call__(self, session, idmap, adaptor=None):
        """Create and or update a sequence of instances.

        :param adaptor: either None or a callable
        :rtype: an iterator over created/referenced instances
        """

        instances = self.data
        if instances is None:
            return

        for data in instances:
            if adaptor is not None:
                data = adaptor(self.model, self.key, data)
            instance = Instance(self, data, idmap)
            yield instance(session, self.delete)


class Instance(object):
    """A single model instance."""

    def __init__(self, entity, data, idmap):
        self.entity = entity
        self.data = data
        self.idmap = idmap
        self.instance = None
        self.created = False

    def __getitem__(self, key):
        item = self.data.get(key, None)
        if id(item) in self.idmap:
            return self.idmap[id(item)]
        else:
            return item

    def __call__(self, session, delete=False):
        "Load an existing instance, create a new one or delete it if it exists"

        from sqlalchemy.orm import object_mapper
        if sys.version_info.major >= 3:
            from itertools import zip_longest
        else:
            from itertools import izip_longest as zip_longest

        if self.instance is not None:
            return self.instance

        model = self.entity.model
        key = self.entity.key

        filter = []
        for fname in key:
            if '->' in fname:
                attrname, _, slot = fname.partition('->')
                fvalue = self[attrname][slot]
            else:
                attrname = fname
                slot = None
                fvalue = self[fname]

            if (sys.version_info.major < 3
                and isinstance(fvalue, basestring)
                and not isinstance(fvalue, unicode)):
                fvalue = fvalue.decode('utf-8')

            if isinstance(fvalue, Instance):
                instance = fvalue(session)

                mapper = object_mapper(instance)
                pkeyf = mapper.primary_key
                pkeyv = mapper.primary_key_from_instance(instance)
                pkey = {f.name: v for f, v in zip_longest(pkeyf, pkeyv)}

                for l, r in getattr(model, attrname).property.local_remote_pairs:
                    filter.append(getattr(model, l.name) == pkey[r.name])
            else:
                attr = getattr(model, attrname)
                if slot is not None:
                    attr = attr[slot]
                filter.append(attr == fvalue)

        q = session.query(model)
        q = q.filter(*filter)
        obj = q.first()

        if delete:
            if obj is not None:
                session.delete(obj)
            return obj

        if obj is None:
            # Create a new one
            obj = model()
            session.add(obj)
            self.created = True

        self.idmap[id(self.data)] = self
        self.instance = obj

        # Update it
        for f in self.data:
            v = self[f]
            if isinstance(v, Instance):
                v = v(session)
            elif isinstance(v, File):
                v = v.read()

            setattr(obj, f, v)

        return obj


def resolve_class_name(classname):
    """Import a particular Python class given its full dotted name.

    :param classname: full dotted name of the class,
                      such as "package.module.ClassName"
    :rtype: the Python class
    """

    modulename, _, classname = classname.rpartition('.')
    module = __import__(modulename, fromlist=[classname])
    return getattr(module, classname)


def load_yaml(fname, session, dry_run=False, delete=False, save_new_instances=False,
              adaptor=None, show_progress=False):
    """Load a single YAML file.

    :param fname: the name of the YAML file to load
    :param session: the SQLAlchemy session
    :param dry_run: whether to commit data at the end
    :param delete: whether instances shall be deleted instead of updated
    :param save_new_instances: if given, the name of the YAML file where
                               information about created instances will be written
    :param adaptor: either None or a function
    :param show_progress: whether to emit some noise as the process goes on
    :rtype: dict
    :returns: A dictionary with loaded data, keyed by (model class, key): each
              value is a tuple (primarykey, datadict)

    This will open the given file (that should contain a UTF-8 encoded
    YAML structure) and will load/update the data into the database, or
    deleted from there.

    The `adaptor` function, if specified, will be called once for each "record"
    and has the opportunity of deliberately change its content::

        user_id = 999

        def adjust_user(cls, key, data):
            if key == ['username']:
                data['username'] = data['username'] + str(user_id)
                data['user_id'] = user_id
            return data

        load_yaml('testdata.yaml', session, adaptor=adjust_user)

    When `delete` is ``True``, then existing instances will be deleted
    from the database instead of created/updated.

    If `save_new_instances` is given, it's a file name that will contain a YAML
    representation of the newly created instances, suitable to be used in a
    subsequent call with `delete` set to ``True``.

    When `dry_run` is ``False`` (the default) the function performs a
    ``flush()`` on the SQLAlchemy session, but does **not** commit the
    transaction.
    """

    from codecs import open
    from sys import stderr
    from sqlalchemy.orm import object_mapper

    if show_progress:
        stderr.write(fname)
        stderr.write(u': ')

    stream = open(fname, 'r', 'utf-8')

    # Set the base directory: file paths will be considered relative
    # to the directory containing the YAML file
    File.basedir = dirname(abspath(fname))

    idmap = {}
    loader = yaml.Loader(stream)
    while loader.check_data():
        entities = loader.get_data()
        for data in entities:
            entity = Entity(data['entity'], data['key'], data.get('data', []), delete)
            for e in entity(session, idmap, adaptor):
                if show_progress:
                    stderr.write('-' if delete and e is not None else '.')

            if not dry_run:
                logger.debug(u"Flushing changes")
                session.flush()

    if show_progress:
        stderr.write('\n')

    if save_new_instances:
        existing_new_instances = set()
        new_new_instances = {}
        if exists(save_new_instances):
            with open(save_new_instances) as f:
                new_instances = yaml.load(f)
            for i in new_instances:
                entity = resolve_class_name(i['entity'])
                keys = i['key']
                for data in i['data']:
                    key = tuple(data[key] for key in keys)
                    existing_new_instances.add((entity, key))
        else:
            new_instances = []

    result = {}
    for i in idmap.values():
        key = []
        for fname in i.entity.key:
            if '->' in fname:
                attr, _, slot = fname.partition('->')
                value = getattr(i.instance, attr)[slot]
            else:
                value = getattr(i.instance, fname)
            key.append(value)
        if len(i.entity.key) == 1:
            key = key[0]
        else:
            key = tuple(key)
        mapper = object_mapper(i.instance)
        pk = mapper.primary_key_from_instance(i.instance)

        if (save_new_instances and i.created
            and (i.entity.model, tuple(pk)) not in existing_new_instances):
            entity = i.entity.model.__module__ + '.' + i.entity.model.__name__
            pknames = tuple(str(c.key) for c in mapper.primary_key)
            data = new_new_instances.setdefault((entity, pknames), [])
            data.append(dict(zip(pknames, pk)))

        if len(pk) == 1:
            pk = pk[0]
        result[(i.entity.model, key)] = pk, i.data

    if save_new_instances and new_new_instances:
        for entity, pknames in sorted(new_new_instances):
            new_instances.append(dict(entity=entity, key=list(pknames),
                                      data=new_new_instances[(entity, pknames)]))
        with open(save_new_instances, 'w') as f:
            yaml.dump(new_instances, f, default_flow_style=False, allow_unicode=True)

    return result


def load(uri, dry_run, echo, delete, save_new_instances, args):
    "Load one or more YAML file into the database."

    from sqlalchemy import create_engine
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(uri, echo=echo)
    salogger = getattr(engine.logger, 'logger', None)
    if salogger is not None:
        for h in salogger.handlers:
            salogger.removeHandler(h)
    smaker = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    session = smaker()

    try:
        for fname in args:
            load_yaml(fname, session, dry_run, delete, save_new_instances,
                      show_progress=not echo)
    except SQLAlchemyError as e:
        # PG errors are UTF-8 encoded
        emsg = str(e)
        if sys.version_info.major < 3:
            emsg = emsg.decode('utf-8')
        logger.error(u"Data couldn't be loaded: %s", emsg)
        return 1
    except Exception:
        logger.exception(u"We are in trouble, unexpected error!")
        return 2
    else:
        if not dry_run:
            logger.info(u"Committing changes")
            session.commit()

    return 0 # OK


def main():
    import locale, logging
    from argparse import ArgumentParser, RawDescriptionHelpFormatter

    locale.setlocale(locale.LC_ALL, '')

    parser = ArgumentParser(
        description="Load and/or update DB model instances.",
        epilog=__doc__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("datafile", nargs="+",
                        help=u"The YAML data file to load.")
    parser.add_argument("-u", "--sqlalchemy-uri", type=str, metavar="URI",
                        help=u"Specify the SQLAlchemy URI.", default=None)
    parser.add_argument("-D", "--delete", default=False, action="store_true",
                        help="Delete existing instances instead of creating/"
                        "updating them. You better know what you are doing!")
    parser.add_argument("-s", "--save-new-instances", type=str, metavar='FILE',
                        help=u"Save new instances information into given YAML file,"
                        " preserving it's previous content.")
    parser.add_argument("-n", "--dry-run", default=False, action="store_true",
                        help=u"Don't commit the changes to the database.")
    parser.add_argument("-e", "--echo", default=False, action="store_true",
                        help=u"Activate SA engine echo")
    parser.add_argument("-d", "--debug", default=False, action="store_true",
                        help=u"Activate debug logging")
    if sys.version_info.major < 3:
        parser.add_argument("-w", "--unicode-warnings", default=False,
                            action="store_true",
                            help=u"Activate SA unicode warnings")

    args = parser.parse_args()

    logging.basicConfig(format='%(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)

    if args.sqlalchemy_uri is None:
        print(u"You must specify the SQLAlchemy URI, example:")
        print(u"  python %s -u postgresql://localhost/dbname data.yaml"
              % sys.argv[0])

        return 128

    if sys.version_info.major < 3 and args.unicode_warnings:
        import warnings
        from sqlalchemy.exc import SAWarning

        warnings.filterwarnings(
            'ignore', category=SAWarning,
            message="Unicode type received non-unicode bind param value")

    return load(args.sqlalchemy_uri, args.dry_run, args.echo,
                args.delete, args.save_new_instances, args.datafile)


if __name__ == '__main__':
    from sys import exit

    exit(main())
