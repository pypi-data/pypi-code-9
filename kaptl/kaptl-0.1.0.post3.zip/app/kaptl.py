import sys

import pyprind
import requests

session = requests.Session()


def parse_rules(rules, stack):
    print "Parsing the rules..."
    request_data = dict(rulesText=rules, stack=stack)
    try:
        response = session.post("https://www.kaptl.com/api/apps/parse", json=request_data)
        response_content = response.json()
        if response.status_code and response_content["success"]:
            print "Rules were parsed successfully"
            return response_content["appName"]
        else:
            print "There was a problem with parsing the rules"
            return None
    except requests.exceptions.RequestException:
        print("API is unavailable at the moment, please try again later")
        sys.exit()


def get_file_info(app_name, stack, rules, angular_only):
    print "Downloading the generated app..."
    request_data = dict(app={
        'id': 0,
        'name': app_name,
        'rules': rules,
        'stack': stack
    }, angularOnly=angular_only)

    try:
        response = session.post("https://www.kaptl.com/api/apps/download", json=request_data)
        response_content = response.json()
        if response.status_code and response_content["success"]:
            return response_content["fileUrl"], response_content["fileName"]
    except requests.exceptions.RequestException:
        print("API is unavailable at the moment, please try again later.")
        sys.exit()


def download_file(file_info):
    with open(file_info[1], 'wb') as f:
        r = session.get(file_info[0], stream=True)
        total_length = int(r.headers.get('content-length'))
        bar = pyprind.ProgBar(total_length / 1024)
        if total_length is None:  # no content length header
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):
                f.write(chunk)
                bar.update()


def read_rules_from_file(path):
    try:
        with open(path) as rules_file:
            return rules_file.read()
    except IOError:
        print "Couldn't read from a file"
        sys.exit()


class NoStackInfoException(Exception):
    pass


class NoRulesInfoException(Exception):
    pass


class Kaptl:
    def __init__(self, arguments):
        self.arguments = arguments

        # process arguments
        if self.arguments["--backend"] is None and self.arguments["--frontend"] is None:
            raise NoStackInfoException("Please specify at least one of the stack parts")

        if self.arguments["--backend"] is not None:
            self.backend = [self.arguments["--backend"]]
        else:
            self.backend = []

        if self.arguments["--frontend"] is not None:
            self.frontend = [self.arguments["--frontend"]]
        else:
            self.frontend = []

        if not self.backend:
            if self.frontend == ["angular"]:
                self.angular_only = True
            else:
                self.angular_only = False
        else:
            self.angular_only = False

        self.stack = {"backend": self.backend, "frontend": self.frontend}

        if self.arguments["<rules>"]:
            self.rules = self.arguments["<rules>"]
        elif self.arguments["--rules-file"]:
            self.rules = read_rules_from_file(self.arguments["--rules-file"])  # read the data from file
        else:
            raise NoRulesInfoException("Couldn't find rules")

    def create_new_app(self):
        app_name = parse_rules(self.rules, self.stack)
        if app_name is not None:
            file_info = get_file_info(app_name, self.stack, self.rules, self.angular_only)
            download_file(file_info)
        else:
            sys.exit()
