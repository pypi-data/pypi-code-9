from flask import request

import json
from django.core.serializers.python import Serializer
from django.core.serializers.json import DjangoJSONEncoder

def limit(request):
    return int(request.args.get('limit', 100))


def offset(request):
    return int(request.args.get('offset', 0))


def order(request, queryset):
    order = request.args.get('order', '').lower()
    sort = request.args.get('sort', '')

    if sort and order and order in ['asc', 'desc']:
        return queryset.order_by('-{}'.format(sort) if order == 'desc' else sort)
    return queryset


def get_fields(request, fields):
    keys = request.args.get('fields', None)

    return dict((k, fields[k]) for k in keys.split(',') if k in fields) if keys else fields


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


# Executa tarefas no celery
@static_vars(celery=None)
def doing_task(task_name, option='delay', args=None):

    # Conecta no celery
    if doing_task.celery is None:
        BROKER_URL = "redis://" + settings.REDIS['HOST'] + ':' + settings.REDIS['PORT'] + '/' + settings.REDIS['DB']
        BACKEND_URL = BROKER_URL
        celery = Celery('DOING', broker=BROKER_URL, backend=BACKEND_URL)

    try:
        if args is not None:
            data = args
        elif request.data:
            try:
                data = json.loads(request.data)
            except:
                data = request.data
        elif request.form:
            data = dict([(k, v[0] if len(v) == 1 else v) for k, v in dict(request.form).items()])
        else:
            data = None

        if not data:
            return 'No data'

        # print(u"Enviando para o celery atraves do broker {} com data = {}".format(celery.conf.BROKER_URL, data))
        if option == 'get':
            celery_response = celery.signature(task_name, kwargs=data).delay().get(timeout=60)
            # print("Recebido do celery!")
            data = json.dumps(celery_response)

            return data
        else:
            celery_response = celery.signature(task_name, kwargs=data).delay()

        if celery_response.status == 'SUCCESS' or celery_response.status == 'PENDING':
            return { 'status': 'SUCCESS', 'code': 200 }
        else:
            return { 'status': 'ERROR', 'code': 500 }

    except TimeoutError:
        return { 'status': 'TIMEOUT', 'code': 408 }


class FlatJsonSerializer(Serializer):
    def get_dump_object(self, obj):
        data = self._current
        if not self.selected_fields or 'id' in self.selected_fields:
            data['id'] = obj.id
        return data
    def end_object(self, obj):
        if not self.first:
            self.stream.write(', ')
        json.dump(self.get_dump_object(obj), self.stream,
                  cls=DjangoJSONEncoder)
        self._current = None
    def start_serialization(self):
        self.stream.write("[")
    def end_serialization(self):
        self.stream.write("]")
    def getvalue(self):
        return super(Serializer, self).getvalue()


def response_format(data):

    object = request.args.get('object',None)

    if object == 'true':
        data = { 'data': data }


    return data