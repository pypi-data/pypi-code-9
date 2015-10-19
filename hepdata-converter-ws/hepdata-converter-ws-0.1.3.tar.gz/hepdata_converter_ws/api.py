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

SINGLEFILE_FORMATS = ['root', 'yoda']

@api.route('/ping', methods=['GET'])
def ping():
    return Response('OK')

@api.route('/convert', methods=['GET'])
def convert():
    kwargs = request.get_json(force=True)
    input_tar = kwargs['input']
    archive_name = kwargs['options'].get('filename', 'hepdata-converter-ws-data')
    output_format = kwargs['options'].get('output_format', '')

    output = StringIO.StringIO()
    if output_format.lower() in SINGLEFILE_FORMATS:
        _os_handle, tmp_output = tempfile.mkstemp()
    else:
        tmp_output = tempfile.mkdtemp()

    tmp_dir = tempfile.mkdtemp()
    try:
        conversion_input = os.path.abspath(tmp_dir)
        conversion_output = os.path.abspath(tmp_output)

        with tarfile.open(mode= "r:gz", fileobj=StringIO.StringIO(base64.decodestring(input_tar))) as tar:
            tar.extractall(path=conversion_input)

        # one file - treat it as one file input format
        walked = list(os.walk(tmp_dir))
        if len(walked) == 1 and len(walked[0][2]) == 1:
            path, dirs, files = walked[0]
            conversion_input = os.path.join(path, files[0])

        else:
            pass
        hepdata_converter.convert(conversion_input + '/' + archive_name + '/',
                                  conversion_output,
                                  kwargs.get('options', {}))

        if not os.path.isdir(conversion_output):
            archive_name = archive_name + '.' + output_format

        with tarfile.open(mode='w:gz', fileobj=output) as tar:
            tar.add(conversion_output, arcname=archive_name)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        shutil.rmtree(tmp_output, ignore_errors=True)

    return Response(output.getvalue(), mimetype='application/x-gzip')
