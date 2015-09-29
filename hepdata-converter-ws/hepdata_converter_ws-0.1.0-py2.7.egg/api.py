# -*- encoding: utf-8 -*-
import StringIO
import base64
import os
import tarfile
import tempfile
from flask.globals import request
from flask.wrappers import Response
import hepdata_converter
import shutil
from flask import current_app, Blueprint, render_template
api = Blueprint('api', __name__)


__author__ = 'Michał Szostak'

@api.route('/ping', methods=['GET'])
def ping():
    return Response('OK')

@api.route('/convert', methods=['GET'])
def convert():
    kwargs = request.get_json(force=True)
    input_tar = kwargs['input']
    output = StringIO.StringIO()

    tmp_output_dir = tempfile.mkdtemp()
    tmp_dir = tempfile.mkdtemp()
    try:
        conversion_input = os.path.abspath(tmp_dir)
        conversion_output = os.path.abspath(tmp_output_dir)

        with tarfile.open(mode= "r:gz", fileobj=StringIO.StringIO(base64.decodestring(input_tar))) as tar:
            tar.extractall(path=conversion_input)

        # one file - treat it as one file input format
        walked = list(os.walk(tmp_dir))
        if len(walked) == 1 and len(walked[0][2]) == 1:
            path, dirs, files = walked[0]
            conversion_input = os.path.join(path, files[0])

        else:
            pass
        hepdata_converter.convert(conversion_input, conversion_output, kwargs.get('options', {}))

        with tarfile.open(mode='w:gz', fileobj=output) as tar:
            tar.add(conversion_output, arcname='hepdata-converter-ws-data')

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        shutil.rmtree(tmp_output_dir, ignore_errors=True)

    return Response(output.getvalue(), mimetype='application/x-gzip')
