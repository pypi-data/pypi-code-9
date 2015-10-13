import os
from flask import Flask
from flask import Response
import models
from xwot.util.vocab import Hydra
from xwot.util.vocab import Owl
from xwot.util.flask import hydra_link
from xwot.util import local_ip
from xwot.util import create_description
from xwot.util import dir_path

from xwot.util.flask import mount_apidoc
from xwot.util.flask import make_response
from xwot.util.vocab import Xwot

from models import annotate

# base config
ip = local_ip()
port = 3000
http_addr = "http://%s:%s/" % (ip, port)
apidoc_url = http_addr + 'vocab'
hydra_link = hydra_link(apidoc_url)


jsonld_description = create_description(xwot_file=os.path.join(dir_path(__file__), "device.xwot"), base=http_addr)


annotate.documentation(entrypoint=http_addr, title='My Api Doc', description='Awesome xWoT Api documentation.',
                       apidoc_url=apidoc_url)

app = Flask(__name__, static_path='')


entrypoint = models.EntryPoint()

"""
Entrypoint controller
"""

"""
    GET EntryPoint
"""
@annotate.route('entry_point', method='GET', description='The APIs main entry point.', returns=Xwot.Resource())
@app.route('/', methods=['GET'])
@hydra_link
def entrypoint_get():
    return make_response(entrypoint)


"""
User controller
"""

"""
    GET User collection
"""
@annotate.route('user_collection_retrieve', method='GET', description='Retrieves all User entities', returns=Hydra.Collection())
@app.route('/users', methods=['GET'])
@hydra_link
def get_user_collection():
    users = models.user_collection
    return make_response(users)




"""
    POST User
"""
@annotate.route('user_create', method='POST', description='Creates a new User entity', returns=Xwot.Resource(),
                expects=Xwot.Resource(), status_codes=[{"code": 201, "description": "If the User entity was created successfully."}])
@app.route('/users', methods=['POST'])
@hydra_link
def post_user(user_id):
    user = models.user_collection.user(user_id)
    if user:
        return make_response(user)
    else:
        return Response(status=404)
"""
    PUT User
"""
@annotate.route('user_replace', method='PUT', description='Replaces a new User entity', returns=Xwot.Resource(),
                expects=Xwot.Resource(), status_codes=[{"code": 201, "description": "If the User entity was created successfully."}])
@app.route('/users', methods=['PUT'])
@hydra_link
def put_user(user_id):
    user = models.user_collection.user(user_id)
    if user:
        return make_response(user)
    else:
        return Response(status=404)


"""
    GET User
"""
@annotate.route('user_retrieve', method='GET', description='Retrieves a User entity', returns=Xwot.Resource(),
                 status_codes=[{"code": 404, "description": "If the User entity wasn't found."}])
@app.route('/users/<int:user_id>', methods=['GET'])
@hydra_link
def get_user(user_id):
    user = models.user_collection.user(user_id)
    if user:
        return make_response(user)
    else:
        return Response(status=404)


"""
    DELETE user
"""
@annotate.route('user_delete', method='DELETE', description='Deletes a User entity', returns=Owl.Nothing(),
                 status_codes=[{"code": 404, "description": "If the User entity wasn't found."}])
@app.route('/users/<int:user_id>', methods=['DELETE'])
@hydra_link
def delete_user(user_id):
    user = models.user_collection.user(user_id)
    if user:
        return ''
    else:
        return Response(status=404)


from xwot.util.apidocbuilder import HydraBuilder
builder = HydraBuilder(annotate)
mount_apidoc(app, builder)
app.debug = True
app.run(host='0.0.0.0', port=port)