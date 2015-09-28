
import os
from datetime import datetime
import sys
# import argparse
# import math

import yaml

from c2.backup.s3.config import info, error
from c2.backup.s3.config import YAML_FIEL_NAME
from c2.backup.s3.upload import upload_to_s3
from c2.backup.s3.listing import get_bucket_list


def get_yaml_data(args_filename):
    yaml_filename = args_filename
    if not os.path.exists(yaml_filename):
        return None
    with open(yaml_filename, 'rb') as f:
        data = yaml.load(f.read())
    return data

def get_yaml_setting(args_filename):
    data = get_yaml_data(args_filename)
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

def get_settings(args_filename):
    yaml_settings = get_yaml_setting(args_filename)
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
    if len(sys.argv) < 2:
        msg = "Invalid args. eg) ./bin/backups3 SUBCOMMAND FAIL_PATH/YAML_FILE_NAME"
        error(msg)
        sys.stdout.write("Error\n\n" + msg + "\n")
        return None, None
    sub_command = sys.argv[1]
    args_filename = " ".join(sys.argv[2:])
    if sub_command not in ('backup', 'list', 'download'):
        msg = "Invalid args. eg) ./bin/backups3 SUBCOMMAND FAIL_PATH/YAML_FILE_NAME\n\
                Sub command is in ('backup', 'list', 'download')"
        error(msg)
        sys.stdout.write("Error\n\n" + msg + "\n")
        return None, None
    out = []
    errors = []
    settings = get_settings(args_filename)
    if settings is None:
        return None, None
    aws_id, aws_key, src_dir, backet_name, backet_path = settings

    if sub_command == "backup":
        info("Starting buckup to the bucket")
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
                    error("Upload error: ${filename}".format(filename=filename))
        out_msg = "Upload files: %{num}".format(num=str(len(out)))
        info(out_msg)
        sys.stdout.write(out_msg + "\n")
        error_msg = "Error files: %{num}".format(num=str(len(errors)))
        info(error_msg)
        sys.stdout.write(error_msg + "\n")
    elif sub_command == "list":
        bucket_list = get_bucket_list(aws_id, aws_key, backet_name, backet_path)
        sys.stdout.write("Listing file on bucket:" + "\n")
        for key in bucket_list:
            data_path = key.name
            out.append(data_path)
            sys.stdout.write(data_path + "\n")
        sys.stdout.write("Done" + "\n")
        info("Listing file on bucket: Done")
    elif sub_command == "download":
        bucket_list = get_bucket_list(aws_id, aws_key, backet_name, backet_path)
        sys.stdout.write("Downloading file from bucket:" + "\n")
        for key in bucket_list:
            data_path = key.name
            filename = data_path.split(backet_path, 1)[1]
            full_path_filename = src_dir + filename
            base_path = os.path.dirname(full_path_filename)
            if not os.path.isdir(base_path):
                os.makedirs(base_path)
            with open(full_path_filename, 'wb') as f:
                key.get_file(f)
        sys.stdout.write("Done: " + src_dir + "\n")
        info("Downloading file from bucket: Done " + src_dir)
    #return out, errors

if __name__ == "__main__":
    res = main()
    # info("success")
    # print(res)
