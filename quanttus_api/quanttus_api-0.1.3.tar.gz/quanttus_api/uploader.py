import argparse
import csv
import datetime
import inspect
import json
import logging
import logging.config
import os
import requests
import sys
import tabulate
import traceback

__author__ = 'jpercent'

level = logging.INFO
logging.basicConfig(level=level)
logger = logging.getLogger("quanttus-upload")


class APIProxy(object):
    def __init__(self, base_url='http://localhost', port=5000):
        super(APIProxy, self).__init__()
        self.base_url = base_url
        self.port = port
        if int(port) != 80:
            self.endpoint = '{0}:{1}'.format(base_url, port)
        else:
            self.endpoint = base_url

    def get_token(self, email, password):
        url = self.endpoint + '/authenticate'
        r = requests.post(url, auth=(email, password))
        if r.status_code >= 400:
            logger.error("token request failed {0}:{1} ".format(r.status_code, r.reason))
            r.raise_for_status()

        token = r.content.decode('utf-8')
        return token

    def get_user_id(self, email, token):
        url = self.endpoint + '/user/search'
        params = {'email': email, 'access_token': token}
        r = requests.get(url, params=params)
        if r.status_code >= 400:
            logger.error("User id request failed {0}:{1} ".format(r.status_code, r.reason))
            r.raise_for_status()

        return json.loads(r.text)['id']

    def upload_file(self, user_id, category, file_id, file_path, token):
        url = self.endpoint + '/log/{user_id}/{category}/{file_id}'.format(
            user_id=user_id, category=category, file_id=file_id)
        params = {'access_token': token}
        files = {'payload': open(file_path, 'rb')}
        r = requests.post(url, files=files, params=params)
        if r.status_code != 201:
            logger.error(("uploading file failed status:reason = {0}:{1}, userid = {2},"+
                         " category = {3}, file_id = {4}, file_path = {5}, token = {6}"
                          ).format(r.status_code, r.reason, user_id,
                                                    category, file_id, file_path, token))
            logger.error("response headers = {0}".format(r.headers))
            logger.error("request headers =  {0}".format(r.request.headers))
            logger.error("request body =  {0}".format(r.request.body))
            r.raise_for_status()
        else:
            logger.debug(("upload file_id = {0}, userid = {1}, category = {2}, "+
                        "file_path = {3}").format(file_id, user_id, category, file_path))
            logger.debug("response content = {0}".format(r.json()))
            return json.loads(r.content.decode('utf-8'))


class ConfException(object):
    pass


class Conf(object):
    def __init__(self, exit_fn=sys.exit, conf=None):
        global logger
        if not conf:
            conf = os.path.join(os.path.dirname(inspect.getfile(Conf)), 'conf.json')

        if not os.path.isfile(conf):
            msg = "embedded, required configuration not found"
            logger.critical(msg)
            raise ConfException(msg)

        parsed_conf = None
        with open(conf, 'rt') as file_descriptor:
            json_string = file_descriptor.read()
            parsed_conf = json.loads(json_string)

        if parsed_conf and 'logger' in parsed_conf:
            logging.config.dictConfig(parsed_conf['logger'])
            logger = logging.getLogger('quanttus-upload')

        if not parsed_conf:
            msg = "embedded, required configuration did not parse"
            logger.critical(msg)
            raise ConfException(msg)

        parser = argparse.ArgumentParser(
            description='Upload a directory through the Quanttus API')
        parser.add_argument('-d', dest='directory', default=None,
                            help='directory to upload. This parameter is required.')
        parser.add_argument('-e', dest='email', default=None, help='User email; required')
        parser.add_argument('-b', dest='base_url', default=None,
                            help='endpoint url')
        parser.add_argument('-p', dest='port', default=None, help='port')
        parser.add_argument('-f', dest='secret_key_path', default=None, help='path to secret key file; required parameter')
        parser.add_argument('-l', dest='logfile_path', default=None, help='log out put to the specified file')
        parser.add_argument('-o', dest='log_level', default=None, help='log level; valid values include debug, info, warn and error')
        cli_args = {k: v for k, v in vars(parser.parse_args()).items() if v is not None}

        parsed_conf.update(cli_args)
        self.__dict__.update(parsed_conf)

        if hasattr(self, 'logfile_path'):
            parsed_conf['logger']['handlers']['file_handler']['filename'] = self.logfile_path
            parsed_conf['logger']['root']['handlers'] = ['console', 'file_handler']
            logging.config.dictConfig(parsed_conf['logger'])
            logger = logging.getLogger('quanttus-upload')

        if hasattr(self, 'log_level'):
            valid_log_levels = ["DEBUG", "INFO","WARN", "WARNING", "ERROR"]
            if not (self.log_level in valid_log_levels):
                logger.error("Invalid log level; valid values include {0}".format(valid_log_levels))
            else:
                parsed_conf['logger']['root']['level'] = self.log_level
                logging.config.dictConfig(parsed_conf['logger'])
                logger = logging.getLogger('quanttus-upload')

        if not hasattr(self, 'base_url') or not hasattr(self, 'port'):
            msg = "missing server information; defaulting to base_url = {0}, port = {1}\n"
            self.base_url = 'http://localhost'
            self.port = 5000
            logger.warning(msg.format(self.base_url, self.port))

        if not hasattr(self, 'directory') or not os.path.isdir(self.directory):
            msg = "A valid directory is required\n"
            logger.critical(msg)
            parser.print_help()
            exit_fn(1)

        if not hasattr(self, 'email'):
            msg = "A valid email is required\n"
            logger.critical(msg)
            parser.print_help()
            exit_fn(1)

        if not hasattr(self, 'secret_key_path'):
            msg = "A valid secret key is required\n"
            logger.critical(msg)
            parser.print_help()
            exit_fn(1)
        else:
            with open(self.secret_key_path) as f:
                self.secret_key = f.read().strip()


class UploadException(Exception):
    pass


class Uploader(object):
    def __init__(self, conf, api_proxy):
        super(Uploader, self).__init__()
        self.proxy = api_proxy
        self.conf = conf
        self.timestamp = datetime.datetime.now()
        self.user_id = None

    def execute(self):
        try:
            self.user_id = self.proxy.get_user_id(self.conf.email, self.conf.secret_key)
        except Exception as e:
            logger.critical("Could not get user id = {0}".format(self.user_id))
            raise UploadException(e)

        responses = []
        for file_name in os.listdir(self.conf.directory):
            file_path = os.path.join(self.conf.directory, file_name)
            if os.path.isfile(file_path):
                if file_name.endswith('.vit'):
                    category = 'device_vital'
                elif file_name.endswith('.raw'):
                    category = 'device_raw'
                else:
                    category = 'unknown_category'
                try:
                    responses.append(self.proxy.upload_file(self.user_id, category, file_name,
                                           file_path, self.conf.secret_key))
                except Exception as e:
                    logger.error("Could not upload file = {0}; error = {1}".format(
                        file_name, traceback.format_exc()))
                    raise UploadException(e)

        write_header_row = True
        if os.path.isfile('output.csv'):
            write_header_row = False

        response_table = []
        with open('output.csv', 'a', newline='') as csvfile:
            csvwritah = csv.writer(csvfile, delimiter='\t', quotechar='|',
                                   quoting=csv.QUOTE_MINIMAL)
            first_response = True
            for r in responses:
                response_table.append([r['fileId'], r['category'], r['url']])
                if write_header_row and first_response:
                    csvwritah.writerow(['fileId', 'category', 'url', 'created','shaHash',
                                       'userId', 'contentType'])

                    first_response = False
                csvwritah.writerow([r['fileId'], r['category'], r['url'],
                                   r['created'], r['shaHash'], r['userId'],
                                   r['contentType']])

        filter_keys = ['fileId', 'category', 'url']
        logger.info("\n"+tabulate.tabulate(response_table, headers=filter_keys))

if __name__ == '__main__':
    conf = Conf()
    proxy = APIProxy(conf.base_url, conf.port)
    Uploader(conf, proxy).execute()
