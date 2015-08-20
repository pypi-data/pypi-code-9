import traceback
from tingyun.api.tracert.time_trace import TimeTrace
from tingyun.api.tracert.database_node import DatabaseNode as Node

import logging

_logger = logging.getLogger(__name__)


class DatabaseTrace(TimeTrace):
    """
    """
    node = Node

    def __init__(self, transaction, sql, dbapi=None, connect_params=None, cursor_params=None, execute_params=None):
        """
        :param transaction:
        :param sql:
        :param dbapi:
        :param connect_params:
        :param cursor_params:
        :param execute_params:
        :return:
        """
        super(DatabaseTrace, self).__init__(transaction)

        self.dbapi = dbapi
        self.connect_params = connect_params
        self.cursor_params = cursor_params
        self.execute_params = execute_params
        self.sql = sql

        self.stack_trace = None
        self.sql_format = None

    def finalize_data(self):
        """create all the data if need
        :return:
        """
        connect_params = None
        cursor_params = None
        execute_params = None
        settings = self.transaction.settings

        if settings.action_tracer.enabled and self.duration >= settings.action_tracer.stack_trace_threshold:
            if self.transaction.stack_trace_count < settings.stack_trace_count:
                self.stack_trace = traceback.extract_stack()
                self.transaction.stack_trace_count += 1

        explain_enabled = settings.action_tracer.explain_enabled
        explain_threshold = settings.action_tracer.explain_threshold
        if settings.action_tracer.enabled and explain_enabled and self.duration > explain_threshold:
            if self.transaction.explain_plan_count < settings.explain_plan_count:
                connect_params = self.connect_params
                cursor_params = self.cursor_params
                execute_params = self.execute_params

        self.sql_format = settings.action_tracer.record_sql
        self.connect_params = connect_params
        self.cursor_params = cursor_params
        self.execute_params = execute_params

    def create_node(self):
        return self.node(dbapi=self.dbapi, sql=self.sql, children=self.children, start_time=self.start_time,
                         end_time=self.end_time, duration=self.duration, exclusive=self.exclusive,
                         stack_trace=self.stack_trace, sql_format=self.sql_format, connect_params=self.connect_params,
                         cursor_params=self.cursor_params, execute_params=self.execute_params)

    def terminal_node(self):
        return True
