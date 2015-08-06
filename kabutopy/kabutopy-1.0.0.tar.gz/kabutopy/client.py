import requests
import os
from io import BytesIO

REGISTER_URL = "/register"
LOGIN_URL = "/login"
POST_IMAGE_URL = "/image"
GET_IMAGE_BUILD_URL = "/image/build/%s"
POST_PIPELINE_URL = "/pipeline"
POST_JOB_URL = "/pipeline/%s/job"
PUT_JOB_URL = "/pipeline/%s/job/%s"
POST_SUBMIT_URL = "/pipeline/%s/submit"
GET_JOB_LOGS_URL = "/execution/%s/logs"
GET_JOB_LOGS_URL2 = "/execution/%s/logs/%s"
GET_JOB_RESULTS = "/pipeline/%s/job/%s?result"

IMAGE_CACHE = {}
PIPELINE_CACHE = {}
JOB_CACHE = {}

CACHE_INDEX = {"Image": IMAGE_CACHE,
               "Pipeline": PIPELINE_CACHE,
               "Job": JOB_CACHE}


class Client(object):
    def __init__(self, service_url):
        if service_url[-1] == "/":
            service_url = service_url[:-1]
        self.url = service_url
        self.cookies = None

    def _build_kwargs(self, url, **kwargs):
        full_url = '%s%s' % (self.url, url)
        kwargs['url'] = full_url
        if self.cookies:
            kwargs['cookies'] = self.cookies
        return kwargs

    def _make_request(self, method, kwargs):
        stop_on_error = kwargs.pop('stop_on_error', True)
        r = method(**kwargs)
        full_url = kwargs['url']
        if not r.status_code == 200:
            msg = "%s did not return a status code 200: %s" % (full_url,
                                                               r.content)
            raise Exception(msg)
        try:
            json = r.json()
            is_dict = isinstance(json, dict)
        except ValueError:
            # there is no json
            is_dict = False

        if stop_on_error and is_dict and json.get('error'):
            raise Exception("%s received an error: %s" % (full_url,
                                                          json['error']))
        return r

    def _post(self, url, **kwargs):
        kwargs = self._build_kwargs(url, **kwargs)
        return self._make_request(requests.post, kwargs)

    def _get(self, url, **kwargs):
        kwargs = self._build_kwargs(url, **kwargs)
        if kwargs.pop("stream", None):
            kwargs['stream'] = True
        return self._make_request(requests.get, kwargs)

    def _put(self, url, **kwargs):
        kwargs = self._build_kwargs(url, **kwargs)
        return self._make_request(requests.put, kwargs)

    def _delete(self, url, **kwargs):
        kwargs = self._build_kwargs(url, **kwargs)
        return self._make_request(requests.delete, kwargs)

    def register(self, user, password, email):
        data = {'login': user,
                'password': password,
                'email': email}
        r = self._post(REGISTER_URL, data=data)
        assert r.json()['status'] == 'success'
        return r.json()['token']

    def login(self, user, password):
        data = {'login': user,
                'password': password}
        r = self._post(LOGIN_URL, data=data)
        self.cookies = r.cookies
        return r.json()['login']

    def _get_id(self, ent, klass):
        if isinstance(ent, klass):
            eid = ent.id
        elif isinstance(ent, int):
            eid = ent
        elif isinstance(ent, str):
            eid = int(ent)
        else:
            msg = "%s id must be an integer or instance" % klass.__name__
            raise Exception(msg)
        return eid

    def create_image(self, name, dockerfile=None, repo_url=None,
                     nocache=False, attachments=None):
        data = {"name": name,
                "nocache": nocache}
        files = self._get_files(attachments)
        if dockerfile:
            content = self._prepare_dockerfile(dockerfile)
            data['dockerfile'] = content
        elif repo_url:
            data['repo_url'] = repo_url
        else:
            raise Exception("The creation of an image requires either "
                            "a dockerfile or a repo_url")
        r = self._post(POST_IMAGE_URL, data=data, files=files)
        return Image(self, r.json()["build_id"], build_id=True)

    def _prepare_dockerfile(self, dockerfile):
        if hasattr(dockerfile, 'read'):
            content = dockerfile.read()
        else:
            if os.path.exists(dockerfile):
                fh = open(dockerfile, 'rb')
                content = fh.read()
            else:
                content = dockerfile
        return content

    def create_pipeline(self, name):
        data = {"name": name}
        r = self._post(POST_PIPELINE_URL, data=data)
        return Pipeline(self, r.json()['id'])

    def create_job(self, command, image, attachments, pipeline):
        image_id = self._get_id(image, Image)
        pipeline_id = self._get_id(pipeline, Pipeline)
        files = self._get_files(attachments)
        data = {"command": command,
                "image_id": image_id}
        r = self._post(POST_JOB_URL % pipeline_id, data=data, files=files)
        pl = Pipeline.load(self, eid=pipeline_id)
        return Job.load(self, eid=r.json()['id'], pipeline=pl)

    def add_job_attachment(self, attachments, job, pipeline):
        job_id = self._get_id(job, Job)
        pipeline_id = self._get_id(pipeline, Pipeline)
        files = self._get_files(attachments)
        self._put(PUT_JOB_URL % (pipeline_id, job_id), files=files)

    def _get_files(self, attachments):
        files = []

        def add_file(item, files):
            if isinstance(item, str):
                if os.path.isfile(item):
                    files.append(("attachments", open(item, "rb")))
                else:
                    raise Exception("%s does not exists")
            elif hasattr(item, 'read'):
                files.append(("attachments", item))
            else:
                raise Exception("%s is not a valid "
                                "attachment type" % type(item))

        if attachments:
            if isinstance(attachments, list):
                for item in attachments:
                    add_file(item, files)
            else:
                add_file(attachments, files)
        return files

    def submit_pipeline(self, pipeline):
        pipeline_id = self._get_id(pipeline, Pipeline)
        if not pipeline.jobs:
            pipeline.refresh()
            if not pipeline.jobs:
                raise Exception("A pipeline needs jobs in order to submit")
        r = self._post(POST_SUBMIT_URL % pipeline_id)
        for job in pipeline.jobs:
            job.state = r.json()[str(job.id)]

    def get_job_logs(self, job, log_id=None):
        job_id = self._get_id(job, Job)
        if log_id:
            url = GET_JOB_LOGS_URL2 % (job_id, log_id)
        else:
            url = GET_JOB_LOGS_URL % job_id

        results = self._get(url)
        lines = results.json()
        return Log(self, job_id, lines)

    def get_job_results(self, job, pipeline=None):
        job_id = self._get_id(job, Job)
        pipeline_id = None
        if pipeline:
            pipeline_id = self._get_id(pipeline, Pipeline)
        else:
            if isinstance(job, Job):
                pipeline_id = job.pipeline_id
        if not pipeline_id:
            raise Exception("Must provide a valid pipeline")
        url = GET_JOB_RESULTS % (pipeline_id, job_id)
        r = self._get(url, stream=True, stop_on_error=False)

        try:
            if r.json().get('error', None):
                return None
        except ValueError:
            # there is no json
            pass

        fh = BytesIO()
        for block in r.iter_content(1024):
            if not block:
                break
            fh.write(block)
        fh.seek(0)
        return fh

    def load_image(self, eid):
        ent = IMAGE_CACHE.get(eid)
        if ent:
            return ent
        return Image.load(self, eid=eid)

    def load_pipeline(self, eid):
        ent = PIPELINE_CACHE.get(eid)
        if ent:
            return ent
        return Pipeline.load(self, eid=eid)

    def load_job(self, eid, pipeline):
        ent = JOB_CACHE.get(eid)
        if ent:
            return ent
        return Job.load(self, eid=eid, pipeline=pipeline)


class Base(object):
    def __init__(self, client, eid, result=None):
        self.client = client
        self.id = str(eid)
        self.init_attrs(result)

    def init_attrs(self, result=None):
        if not result:
            url = self._make_get_url()
            result = self.client._get(url).json()[str(self.id)]
        for field in self.fields:
            val = result.get(field)
            if val:
                setattr(self, field, val)

    def _make_get_url(self):
        raise NotImplementedError

    @classmethod
    def load(cls, client, eid=None, force=False, **kwargs):
        ent = CACHE_INDEX[cls.__name__].get(eid)
        if ent and not force:
            return ent
        if eid:
            return cls(client, eid, **kwargs)
        else:
            results = client._get(cls.GET_ALL_URL % kwargs).json()
            entities = []
            for eid, result in results.items():
                entities.append(cls(client, eid, result=result))
            return entities

    def refresh(self):
        self.init_attrs()

    def delete(self):
        url = self._make_get_url()
        self.client._delete(url)


class Image(Base):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    PENDING = 'PENDING'
    GET_URL = '/image/%s'
    GET_ALL_URL = '/image'
    fields = ["id", "name", "dockerfile", "creation_date"]

    def __init__(self, client, eid, build_id=False, result=None):
        IMAGE_CACHE[eid] = self
        self.client = client
        self.error = None
        self.build_output = None
        if not build_id:
            self._id = str(eid)
            self.build_id = None
            self._status = self.SUCCESS
            self.init_attrs(result)
        else:
            self._id = None
            self.build_id = eid
            self._status = self.PENDING

    def _make_get_url(self):
        return self.GET_URL % self.id

    def _poll_server(self):
        r = self.client._get(GET_IMAGE_BUILD_URL % self.build_id,
                             stop_on_error=False)
        res = r.json()
        print(res)
        self._status = res.get('state')
        if self._status == self.SUCCESS:
            self._id = str(res['id'])
            self.init_attrs()
            IMAGE_CACHE[self._id] = self
        if res.get('error'):
            self.error = res.get('error')
            if not self._status:
                self._status = 'FAILED'
        if res.get('output'):
            self.build_output = res.get('output')

    def init_attrs(self, result=None):
        url = self._make_get_url()
        if not result:
            result = self.client._get(url).json()[self.id]
        for field in self.fields:
            attr = field
            if field == "id":
                attr = "_id"
            val = result.get(field)
            if val:
                setattr(self, str(attr), val)

    @property
    def id(self):
        if self._id:
            return self._id
        if self.FAIL in self._status:
            return None
        self._poll_server()
        return self._id

    @property
    def status(self):
        if self._status == self.SUCCESS:
            return self._status
        if self.FAIL in self._status:
            return self._status
        self._poll_server()
        return self._status

    @classmethod
    def load(cls, client, eid=None, build_id=False):
        return super(Image, cls).load(client, eid=eid, build_id=build_id)


class Pipeline(Base):
    GET_URL = "/pipeline/%s"
    GET_ALL_URL = "/pipeline"
    fields = ["id", "name", "creation_date", "jobs"]

    def __init__(self, client, eid, result=None):
        PIPELINE_CACHE[eid] = self
        super(Pipeline, self).__init__(client, eid, result=result)
        self.jobs = self.get_jobs()

    def _make_get_url(self):
        return self.GET_URL % self.id

    def submit(self):
        self.client.submit_pipeline(self)

    def get_jobs(self):
        return Job.load(self.client, pipeline_id=self.id)


class Job(Base):
    GET_URL = "/pipeline/%s/job/%s"
    GET_ALL_URL = "/pipeline/%(pipeline_id)s/job"
    fields = ["id", "command", "state", "creation_date",
              "used_cpu", "used_memory", "used_io", "attachment_token",
              "results_path", "image", "pipeline"]

    def __init__(self, client, eid, pipeline=None, result=None):
        JOB_CACHE[eid] = self
        self._image_id = None
        self._pipeline = None
        self._image = None
        if pipeline:
            self._pipeline_id = pipeline.id
            self.pipeline = pipeline
            pipeline.jobs.append(self)
        super(Job, self).__init__(client, eid, result=result)

    def _make_get_url(self):
        return self.GET_URL % (self.pipeline_id, self.id)

    def get_logs(self, log_id=None):
        return self.client.get_job_logs(self, log_id)

    def get_results(self):
        return self.client.get_job_results(self)

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def image(self):
        return self._image

    @pipeline.setter
    def pipeline(self, value):
        self._pipeline = self._set_entity(value, Pipeline)

    @image.setter
    def image(self, value):
        self._image = self._set_entity(value, Image)

    def _set_entity(self, value, klass):
        attr = None

        def load(klass, eid):
            return klass.load(self.client, eid=eid)

        if isinstance(value, dict):
            attr = load(klass, value["id"])
        elif isinstance(value, int) or isinstance(value, str):
            attr = load(klass, value)
        elif isinstance(value, klass):
            attr = value
        return attr

    @property
    def pipeline_id(self):
        return self.pipeline.id

    @property
    def image_id(self):
        return self.image.id

    def add_attachments(self, attachments):
        return self.client.add_job_attachment(attachments, self.id,
                                              self.pipeline.id)


class Log(object):
    def __init__(self, client, job_id, lines):
        self.client = client
        self.lines = []
        self.job_id = str(job_id)
        for line in lines:
            self.lines.append((line['id'], line['logline']))

    def readlines(self, raw=True):
        for line in self.lines:
            if raw:
                yield line[1]
            else:
                yield line

    def refresh(self):
        last_log_id = self.lines[-1][0]
        logs = self.client.get_job_logs(self.job_id, last_log_id)
        self.lines = self.lines + logs.lines
