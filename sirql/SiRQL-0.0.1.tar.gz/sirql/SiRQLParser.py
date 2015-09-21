import re
from sirql.SiRQLCondition import SiRQLCondition


class SiRQLParser(object):
    # Regex: https://regex101.com/r/oL9lC0/1
    __operator_regex = re.compile(ur'(?P<not>not_)?(?P<operator>\w+)\(')

    @staticmethod
    def parse(request_arguments):
        conditions = map(lambda (k, v): SiRQLParser.__parse_request_parameter(k, v), request_arguments.items())
        return conditions

    @staticmethod
    def __parse_request_parameter(key, value):

        field = key
        not_prefix, operator = SiRQLParser.__read_operator(value)
        params = SiRQLParser.__read_parameter(value)

        return SiRQLCondition.init(field, operator, not_prefix, *params)

    @staticmethod
    def __read_operator(text):
        match = SiRQLParser.__operator_regex.search(text)

        not_prefix = bool(match.group('not'))
        operator = match.group('operator')

        return not_prefix, operator

    @staticmethod
    def __read_parameter(text):
        parameter = []
        parse_buffer = ''

        in_param = False
        in_string = False
        in_escape = False

        for c in text:
            if c == '(' and not in_string:
                in_param = not in_param
                continue

            if c == ')' and not in_string:
                parameter.append(parse_buffer.strip())
                break

            if not in_param:
                continue

            if c == '\\' and in_string and not in_escape:
                in_escape = True
                continue

            if c == '"' and not in_escape:
                in_string = not in_string
                parse_buffer += "'"
                continue

            if c == ',' and not in_string:
                parameter.append(parse_buffer.strip())
                parse_buffer = ''
                continue

            if in_param:
                if in_escape:
                    in_escape = False
                parse_buffer += c

        return parameter
