
import os
from datetime import datetime
import sys
# import argparse
# import math

import yaml

from c2.backup.s3.config import info, error
from c2.backup.s3.config import YAML_FIEL_NAME
from c2.backup.s3.upload import upload_to_s3


def get_yaml_data():
    if len(sys.argv) > 1:
        args_filename = " ".join(sys.argv[1:])
        yaml_filename = args_filename
    else:
        yaml_filename = YAML_FIEL_NAME
    if not os.path.exists(yaml_filename):
        return None
    with open(yaml_filename, 'rb') as f:
        data = yaml.load(f.read())
    return data

def get_yaml_setting():
    data = get_yaml_data()
    if data is None:
        return None
    return data

def get_aws_setting(data):
    aws_setting = data.get('aws')
    if aws_setting is None:
        return None, None
    aws_id = aws_setting.get('id')
    aws_key = aws_setting.get('key')
    return aws_id, aws_key

def get_src_setting(data):
    src_setting = data.get('src')
    if src_setting is None:
        return None
    dir_ = src_setting.get('dir')
    return dir_

def get_dist_setting(data):
    dist_setting = data.get('dist')
    if dist_setting is None:
        return None, None
    backet_name = dist_setting.get('backet_name')
    path = dist_setting.get('path')
    return backet_name, path

def get_settings():
    yaml_settings = get_yaml_setting()
    if yaml_settings is None:
        msg = 'No yaml file or invalid file. Please put `c2backups3.yaml` on current directory'
        error(msg)
        return None
    aws_id, aws_key = get_aws_setting(yaml_settings)
    src_dir = get_src_setting(yaml_settings)
    backet_name, backet_path = get_dist_setting(yaml_settings)
    if aws_id is None or aws_key is None or\
           src_dir is None or backet_name is None or backet_path is None:
        msg = 'Invalid yaml file. Please make sure `c2backups3.yaml` on current directory'
        error(msg)
        return None
    return aws_id, aws_key, src_dir, backet_name, backet_path

def get_src_files(src_dir):
    for p, subdirs, files in os.walk(src_dir):
        for f in files:
            yield os.path.join(p, f)


def main():
    out = []
    errors = []
    settings = get_settings()
    if settings is None:
        return None, None
    aws_id, aws_key, src_dir, backet_name, backet_path = settings
    src_dir_len = len(src_dir)
    now = datetime.now()
    base_path = backet_path + "/" + now.strftime('%Y%m%d%H%M') + "/"
    files = get_src_files(src_dir)
    for filename in files:
        path = base_path + filename[src_dir_len:]
        with open(filename, "rb") as fileobj:
            res = upload_to_s3(aws_id, aws_key, fileobj, backet_name, path)
            if res:
                out.append(filename)
            else:
                errors.append(filename)
    return out, errors

if __name__ == "__main__":
    res = main()
    # info("success")
    # print(res)
