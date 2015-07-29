# -*- coding: utf-8 -*-
"""bill and other documents parser

Usage:
    billparser [options] <billfile>

Options:
    -l LIBRARY_DIR   Folder where find parse library files
    -h --help        Show this screen.
"""
import subprocess
import os
import json
import re
import datetime

__version__ = '0.1'

DEFAULT_LIBRARY_PATH = "/etc/billparser/library"


class RegexField:
    def __init__(self, field_def):
        if isinstance(field_def, basestring):
            self.regex = re.compile(field_def, re.MULTILINE)
        else:
            flags = [getattr(re, flag) for flag in field_def.get("flags", [])]
            flags = sum(flags) + re.MULTILINE
            self.regex = re.compile(field_def["regex"], flags)

    def parse(self, bill_as_text):
        match = self.regex.search(bill_as_text)
        if not match:
            return None
        if match.groupdict():
            return match.groupdict()
        if not match.groups():
            return match.group()
        elif len(match.groups()) == 1:
            return match.group(1)
        else:
            return match.groups()


class FloatRegexField(RegexField):
    def parse(self, bill_as_text):
        value_as_string = RegexField.parse(self, bill_as_text)
        if value_as_string:
            if type(value_as_string) == tuple and len(value_as_string) == 2:
                return float(value_as_string[0]) + float(value_as_string[1]) / 100.0
            return float(value_as_string)


class IntRegexField(RegexField):
    def parse(self, bill_as_text):
        value_as_string = RegexField.parse(self, bill_as_text)
        if value_as_string:
            return int(value_as_string)


class DateRegexField(RegexField):
    months = ["ene,feb,mar,abr,may,jun,jul,ago,sep,oct,nov,dic".split(","),
              "january,february,march,april,may,june,july,august,september,november,december".split(","),
              "jan,feb,mar,apr,may,jun,jul,aug,sep,nov,dec".split(","),
              "enero,febrero,marzo,abril,mayo,junio,julio,agosto,septiembre,noviembre,diciembre".split(","),
              ]

    def _parse_month(self, m):
        m = m.lower()
        for months in self.months:
            if m in months:
                return months.index(m.lower()) + 1
        raise ValueError("'%s' no es un mes válido" % m)

    def parse(self, bill_as_text):
        value = RegexField.parse(self, bill_as_text)
        if value:
            if isinstance(value, dict):
                if len(value["month"]) >= 3:
                    month = self._parse_month(value["month"])
                else:
                    month = value["month"]
                day, month, year = int(value["day"]), int(month), int(value["year"])
            else:
                if type(value) == tuple and len(value) >= 3:
                    if len(value[1]) == 3:
                        month = self._parse_month(value[1])
                        value = value[0], month, value[2]
                    value = "%s/%s/%s" % value
                day, month, year = map(int, value.split("/"))
            if year < 100:
                year += 2000
            return datetime.date(year, month, day)


class ConstantField:
    def __init__(self, field_def):
        self.constant = field_def["value"]

    def parse(self, bill_as_text):
        return self.constant


class MultipleField:

    def __init__(self, field_def):
        self.value = field_def["value"]

    def parse(self, bill_as_text, fields):
        return self.value % fields


class FallbackField:

    def __init__(self, field_def):
        self.value = field_def["value"]

    def parse(self, bill_as_text, fields):
        for field_name in self.value.split(","):
            if fields.get(field_name, None) is not None:
                return fields[field_name]


def make_field(field_def):
    if isinstance(field_def, basestring) or "type" not in field_def:
        return RegexField(field_def)
    else:
        return globals()[field_def["type"]](field_def)


def parse_bill(library_file, bill_as_text):
    ret = {}
    multiple_fields = []
    for field_name, field_def in library_file["fields"].items():
        field = make_field(field_def)
        if type(field_def) == dict and field_def.get("type") in("MultipleField", "FallbackField"):
            multiple_fields.append((field_name, field))
        else:
            ret[field_name] = field.parse(bill_as_text)
    for field_name, field in multiple_fields:
        ret[field_name] = field.parse(bill_as_text, ret)
    return ret


def billparser(bill_file, library_dir=DEFAULT_LIBRARY_PATH):
    if bill_file.endswith(".pdf"):
        bill_as_text = subprocess.check_output(["pdftotext", bill_file, "-"])
        bill_as_text = unicode(bill_as_text, "utf-8")
    else:
        bill_as_text = open(bill_file).read()

    for library_file in sorted(os.listdir(library_dir)):
        if not library_file.endswith(".json"):
            continue
        library_file = json.load(open(os.path.join(library_dir, library_file)))
        if make_field(library_file["match"]).parse(bill_as_text):
            return parse_bill(library_file, bill_as_text)
    return None


def _json_converter(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


def main():
    from docopt import docopt
    arguments = docopt(__doc__, version=__version__)
    ret = billparser(arguments['<billfile>'],
                     arguments.get("-l") or DEFAULT_LIBRARY_PATH)
    print(json.dumps(ret, default=_json_converter))


if __name__ == '__main__':
    main()
