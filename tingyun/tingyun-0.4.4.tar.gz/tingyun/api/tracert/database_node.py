from collections import namedtuple
from tingyun.api.tracert.database_utils import sql_statement
from tingyun.api.tracert.attribution import node_start_time, node_end_time, TimeMetric
from tingyun.api.settings import global_settings

_SlowSqlNode = namedtuple('_SlowSqlNode', ['duration', 'path', 'request_uri', 'sql', 'sql_format', 'metric', 'dbapi',
                                           'stack_trace', 'connect_params', 'cursor_params', 'execute_params',
                                           "start_time"])
_DatabaseNode = namedtuple('_DatabaseNode', ['dbapi',  'sql', 'children', 'start_time', 'end_time', 'duration',
                                             'exclusive', 'stack_trace', 'sql_format', 'connect_params',
                                             'cursor_params', 'execute_params'])

import logging

_logger = logging.getLogger(__name__)


class SlowSqlNode(_SlowSqlNode):
    """
    """
    def __new__(cls, *args, **kwargs):
        node = _SlowSqlNode.__new__(cls, *args, **kwargs)
        node.statement = sql_statement(node.sql, node.dbapi)
        return node

    @property
    def formatted(self):
        return self.statement.formatted(self.sql_format)

    @property
    def identifier(self):
        return self.statement.identifier

    @property
    def explain_plan(self):
        return self.statement.explain_plan(self.connect_params, self.cursor_params, self.execute_params)


class DatabaseNode(_DatabaseNode):

    def __new__(cls, *args, **kwargs):
        node = _DatabaseNode.__new__(cls, *args, **kwargs)
        node.statement = sql_statement(node.sql, node.dbapi)

        return node

    @property
    def operation(self):
        return self.statement.operation

    @property
    def target(self):
        return self.statement.target

    @property
    def formatted(self):
        return self.statement.formatted(self.sql_format)

    @property
    def explain_plan(self):
        return self.statement.explain_plan(self.connect_params, self.cursor_params, self.execute_params)

    def time_metrics(self, root, parent):
        """
        :param root:
        :param parent:
        :return:
        """
        name = 'GENERAL/Database/NULL/All'
        yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

        if root.type == 'WebAction':
            name = "GENERAL/Database/NULL/AllWeb"
            yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)
        else:
            name = "GENERAL/Database/NULL/AllBackgound"
            yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

        operation = str(self.operation).upper()

        if operation in ('SELECT', 'UPDATE', 'INSERT', 'DELETE'):
            if self.target:
                name = "GENERAL/Database/%s/%s" % (self.target, operation)
                yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

                name = "Database/%s/%s" % (self.target, operation)
                yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

            name = "GENERAL/Database/NULL/%s" % operation
            yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)
        else:
            name = "GENERAL/Database/operation/CALL"
            yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

            name = "Database/operation/CALL"
            yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

    def trace_node(self, root):
        """
        :param root: the root node of the transaction
        :return:
        """
        params = {"sql": "", "explainPlan": {}, "stacktrace": []}
        children = []
        call_count = 1
        class_name = ""
        method_name = root.name
        call_url = ""
        root.trace_node_count += 1
        start_time = node_start_time(root, self)
        end_time = node_end_time(root, self)
        operation = str(self.operation).upper()
        metric_name = "Database/CALL/sql"

        if operation in ('SELECT', 'UPDATE', 'INSERT', 'DELETE'):
            metric_name = 'Database/%s/%s' % (self.target, operation) if self.target else 'Database/NULL/%s' % operation

        if self.formatted:
            # Note, use local setting only.
            _settings = global_settings()
            params['sql'] = self.formatted

            if _settings.action_tracer.log_sql:
                _logger.info("Log sql is opened. sql upload is disabled, sql sentence is %s", self.formatted)
                params['sql'] = ""

            if self.explain_plan:
                params['explainPlan'] = self.explain_plan

            if self.stack_trace:
                for line in self.stack_trace:
                    if len(line) >= 4:
                        params['stacktrace'].append("%s(%s:%s)" % (line[2], line[0], line[1]))

        return [start_time, end_time, metric_name, call_url, call_count, class_name, method_name, params, children]

    def slow_sql_node(self, root):
        """
        :return:
        """
        request_uri = root.request_uri.replace("%2F", "/")
        metric_name = "Database/CALL/sql"
        operation = str(self.operation).upper()

        if operation in ('SELECT', 'UPDATE', 'INSERT', 'DELETE'):
            metric_name = 'Database/%s/%s' % (self.target, operation) if self.target else 'Database/NULL/%s' % operation

        return SlowSqlNode(duration=self.duration, path=root.path, request_uri=request_uri, metric=metric_name,
                           start_time=self.start_time, sql=self.sql, sql_format=self.sql_format, dbapi=self.dbapi,
                           stack_trace=self.stack_trace, connect_params=self.connect_params,
                           cursor_params=self.cursor_params, execute_params=self.execute_params)
