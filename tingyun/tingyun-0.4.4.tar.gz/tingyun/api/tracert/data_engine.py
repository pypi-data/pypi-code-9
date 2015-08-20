"""this module is implement to deal the transaction all data

"""
import copy

import logging
import threading
from tingyun.api.tracert.stats import TimeStats, ApdexStats, SlowSqlStats
from tingyun.api.platform import six


_logger = logging.getLogger(__name__)


class DataEngine(object):
    """
    """
    def __init__(self):
        self.__max_error_count = 10
        self.__settings = None

        self.__time_stats = {}  # store time stats data key is name + scope
        self.__apdex_stats = {}
        self.__action_stats = {}
        self.__general_stats = {}
        # it's maybe include {name: {transactionType, count, $ERROR_COUNTERS_ITEM}}
        # $ERROR_ITEM  detail, check the documentation
        self.__traced_errors = {}

        # format: {$"metric_name": [$slow_action_data, $duration]}
        self.__slow_action = {}

        self.__slow_sql_stats = {}

        self._stats_lock = threading.Lock()

    @property
    def settings(self):
        """
        :return:
        """
        return self.__settings

    def create_data_zone(self):
        """create empty data engine to contain the unmerged transaction data
        :return:
        """
        zone = DataEngine()
        zone.__settings = self.__settings

        return zone

    def reset_stats(self, application_settings):
        """
        :param application_settings: application settings from server and setting file
        :return:
        """
        self.__settings = application_settings

        self.__time_stats = {}
        self.__apdex_stats = {}
        self.__action_stats = {}
        self.__general_stats = {}
        self.__traced_errors = {}
        self.__slow_action = {}
        self.__slow_sql_stats = {}

    def record_transaction(self, transaction):
        """
        :param transaction: transaction node instance
        :return:
        """
        if not self.__settings:
            _logger.error("The application settings is not merge into data engine.")
            return

        node_limit = self.__settings.action_tracer_nodes

        self.record_time_metrics(transaction.time_metrics())  # deal for component, include framework/db/other
        self.record_action_metrics(transaction.action_metrics())  # deal for user action
        self.record_apdex_metrics(transaction.apdex_metrics())  # for recording the apdex
        self.record_traced_errors(transaction.traced_error())  # for error trace detail
        self.record_slow_action(transaction.slow_action_trace(node_limit))
        self.record_slow_sql(transaction.slow_sql_nodes())

    def record_slow_sql(self, nodes):
        """
        :param nodes: the slow sql node
        :return:
        """
        if not self.__settings.action_tracer.slow_sql:
            return

        for node in nodes:
            key = node.identifier
            stats = self.__slow_sql_stats.get(key)
            if not stats and len(self.__slow_sql_stats) < self.__settings.slow_sql_count:
                stats = SlowSqlStats()
                self.__slow_sql_stats[key] = stats

            if stats:
                stats.merge_slow_sql_node(node)

    def record_slow_action(self, slow_action):
        """
        :param slow_action:
        :return:
        """
        if not self.__settings.action_tracer.enabled:
            return

        threshold = self.__settings.action_tracer.action_threshold
        top_n = self.__settings.action_tracer.top_n
        if slow_action[1] < threshold:
            return

        if len(self.__slow_action) > top_n:
            _logger.debug("The slow action trace is reach the top, action(%s) is ignored.", slow_action[2])
            return

        metric_name = slow_action[2]
        if metric_name not in self.__slow_action:
            self.__slow_action[metric_name] = [slow_action, slow_action[1]]
        else:
            if slow_action[1] > self.__slow_action[metric_name][1]:
                self.__slow_action[metric_name] = [slow_action, slow_action[1]]

    def record_traced_errors(self, traced_errors):
        """
        :return:
        """
        if not self.__settings.error_collector.enabled:
            return

        for error in traced_errors:
            if len(self.__traced_errors) > self.__max_error_count:
                _logger.debug("Error trace is reached maximum limitation.")
                break

            if error.error_filter_key in self.__traced_errors:
                self.__traced_errors[error.error_filter_key]["count"] += 1
                self.__traced_errors[error.error_filter_key]["item"][-3] += 1
            else:
                self.__traced_errors[error.error_filter_key] = {"count": 1, "item": error.trace_data,
                                                                "transaction_type": error.transaction_type}

    def record_general_metric(self, metric):
        """
        :param metric:
        :return:
        """
        key = (metric.name.split("/", 1)[1], '')

        stats = self.__general_stats.get(key)
        if stats is None:
            stats = TimeStats()

        stats.merge_time_metric(metric)
        self.__general_stats[key] = stats

        return key

    def record_time_metric(self, metric):
        """
        :param metric:
        :return:
        """
        # filter the general data from the metric, the metric node should be distinguish general and basic metric
        if metric.name.startswith("GENERAL"):
            self.record_general_metric(metric)
            return

        key = (metric.name, metric.scope or '')  # metric key for protocol
        stats = self.__time_stats.get(key)
        if stats is None:
            stats = TimeStats()

        stats.merge_time_metric(metric)
        self.__time_stats[key] = stats

        return key

    def record_time_metrics(self, metrics):
        """
        :param metrics:
        :return:
        """
        for metric in metrics:
            self.record_time_metric(metric)

    def record_apdex_metric(self, metric):
        """
        :param metric:
        :return:
        """
        key = (metric.name, "")
        stats = self.__apdex_stats.get(key)

        if stats is None:
            stats = ApdexStats(apdex_t=metric.apdex_t)

        stats.merge_apdex_metric(metric)
        self.__apdex_stats[key] = stats
        return key

    def record_apdex_metrics(self, metrics):
        """
        :param metrics:
        :return:
        """
        for metric in metrics:
            self.record_apdex_metric(metric)

    def record_action_metric(self, metric):
        """
        :param metric:
        :return:
        """
        key = (metric.name, metric.scope or '')  # metric key for protocol
        stats = self.__action_stats.get(key)
        if stats is None:
            stats = TimeStats()

        stats.merge_time_metric(metric)
        self.__action_stats[key] = stats

        return key

    def record_action_metrics(self, metrics):
        """
        :param metrics:
        :return:
        """
        for metric in metrics:
            self.record_action_metric(metric)

    def rollback(self, stat, merge_performance=True):
        """rollback the performance data when upload the data failed. except the traced error count.
        :param stat:
        :param merge_performance:
        :return:
        """
        if not merge_performance:
            return

        _logger.warning("Agent will rollback the data which is captured at last time. That indicates your network is"
                        " broken.")

        for key, value in six.iteritems(stat.__time_stats):
            stats = self.__time_stats.get(key)
            if not stats:
                self.__time_stats[key] = copy.copy(value)
            else:
                stats.merge_stats(value)

        for key, value in six.iteritems(stat.__apdex_stats):
            stats = self.__apdex_stats.get(key)
            if not stats:
                self.__apdex_stats[key] = copy.copy(value)
            else:
                stats.merge_stats(value)

        for key, value in six.iteritems(stat.__action_stats):
            stats = self.__action_stats.get(key)
            if not stats:
                self.__action_stats[key] = copy.copy(value)
            else:
                stats.merge_stats(value)

        for key, value in six.iteritems(stat.__general_stats):
            stats = self.__general_stats.get(key)
            if not stats:
                self.__general_stats[key] = copy.copy(value)
            else:
                stats.merge_stats(value)

        for key, value in six.iteritems(stat.__traced_errors):
            stats = self.__traced_errors.get(key)
            if not stats:
                self.__traced_errors[key] = copy.copy(value)
            else:
                stats["count"] += value["count"]

    def merge_metric_stats(self, snapshot):
        """
        :param snapshot:
        :return:
        """
        for key, value in six.iteritems(snapshot.__time_stats):
            stats = self.__time_stats.get(key)
            if not stats:
                self.__time_stats[key] = copy.copy(value)
            else:
                stats.merge_stats(value)

        for key, value in six.iteritems(snapshot.__apdex_stats):
            stats = self.__apdex_stats.get(key)
            if not stats:
                self.__apdex_stats[key] = copy.copy(value)
            else:
                stats.merge_stats(value)

        for key, value in six.iteritems(snapshot.__action_stats):
            stats = self.__action_stats.get(key)
            if not stats:
                self.__action_stats[key] = copy.copy(value)
            else:
                stats.merge_stats(value)

        # TODO: think more about the background task
        for key, value in six.iteritems(snapshot.__traced_errors):
            stats = self.__traced_errors.get(key)
            if not stats:
                self.__traced_errors[key] = copy.copy(value)
            else:
                stats["count"] += value["count"]

        # generate general data
        for key, value in six.iteritems(snapshot.__general_stats):
            stats = self.__general_stats.get(key)
            if not stats:
                self.__general_stats[key] = copy.copy(value)
            else:
                stats.merge_stats(value)

        # for slow action
        top_n = self.__settings.action_tracer.top_n
        for key, value in six.iteritems(snapshot.__slow_action):
            if len(self.__slow_action) > top_n:
                _logger.debug("The slow action trace count is reach the top.")
                break

            slow_acton = self.__slow_action.get(key)
            if not slow_acton:
                self.__slow_action[key] = value[0]
            else:
                if slow_acton[1] < value[1]:
                    self.__slow_action[key] = value[0]

        # for slow sql
        max_sql = self.__settings.slow_sql_count
        for key, value in six.iteritems(snapshot.__slow_sql_stats):
            if len(self.__slow_sql_stats) > max_sql:
                _logger.debug("The slow sql trace count is reach the top.")

            slow_sql = self.__slow_sql_stats.get(key)
            if not slow_sql:
                self.__slow_sql_stats[key] = value
            else:
                if value.slow_sql_node.duration > slow_sql.slow_sql_node.duration:
                    self.__slow_sql_stats[key] = value

    def reset_metric_stats(self):
        """
        :return:
        """
        self.__time_stats = {}  # component
        self.__apdex_stats = {}
        self.__action_stats = {}
        self.__general_stats = {}

        self.__traced_errors = {}
        self.__slow_action = {}
        self.__slow_sql_stats = {}

    def stats_snapshot(self):
        """
        :return:
        """
        stat = copy.copy(self)

        self.__time_stats = {}
        self.__action_stats = {}
        self.__apdex_stats = {}
        self.__traced_errors = {}
        self.__general_stats = {}
        self.__slow_action = {}
        self.__slow_sql_stats = {}

        return stat

    # just for upload performance package
    # strip to 5 parts
    def component_metrics(self, metric_name_ids):
        """
        :return:
        """
        result = []

        for key, value in six.iteritems(self.__time_stats):
            upload_key = {"name": key[0], "parent": key[1]}
            upload_key_str = '%s:%s' % (key[0], key[1])
            upload_key = upload_key if upload_key_str not in metric_name_ids else metric_name_ids[upload_key_str]
            result.append([upload_key, value])

        return result

    def apdex_data(self, metric_name_ids):
        """
        :return:
        """
        result = []

        for key, value in six.iteritems(self.__apdex_stats):
            upload_key = {"name": key[0]}
            upload_key_str = '%s' % key[0]
            upload_key = upload_key if upload_key_str not in metric_name_ids else metric_name_ids[upload_key_str]
            result.append([upload_key, value])

        return result

    def action_metrics(self, metric_name_ids):
        """
        :return:
        """
        result = []
        for key, value in six.iteritems(self.__action_stats):
            upload_key = {"name": key[0]}
            upload_key_str = '%s' % key[0]
            upload_key = upload_key if upload_key_str not in metric_name_ids else metric_name_ids[upload_key_str]
            result.append([upload_key, value])

        return result

    def error_stats(self, metric_name_ids):
        """stat the error trace metric for performance
        :return:
        """
        error_count = {
            "Errors/Count/All": 0,
            "Errors/Count/AllWeb": 0,
            "Errors/Count/AllBackground": 0
        }

        for error_filter_key, error in six.iteritems(self.__traced_errors):
            error_count["Errors/Count/All"] += error["count"]

            if error["transaction_type"] == "WebAction":
                error_count["Errors/Count/AllWeb"] += error["count"]

                action_key = "Errors/Count/%s" % error_filter_key.split("_|")[0]
                if action_key not in error_count:
                    error_count[action_key] = error["count"]
                else:
                    error_count[action_key] += error["count"]
            else:
                error_count["Errors/Count/AllBackground"] += 1

        stat_value = []
        for key, value in six.iteritems(error_count):
            upload_key = {"name": key}
            upload_key_str = '%s' % key
            upload_key = upload_key if upload_key_str not in metric_name_ids else metric_name_ids[upload_key_str]
            stat_value.append([upload_key, [value]])

        return stat_value

    # stat for error trace data
    # rely to the basic error trace data structure
    def error_trace_data(self):
        """
        :return:
        """
        return [error["item"] for error in six.itervalues(self.__traced_errors)]

    def general_trace_metric(self, metric_name_ids):
        """
        :return:
        """
        result = []
        for key, value in six.iteritems(self.__general_stats):
            upload_key = {"name": key[0]}
            upload_key_str = '%s' % key[0]
            upload_key = upload_key if upload_key_str not in metric_name_ids else metric_name_ids[upload_key_str]
            result.append([upload_key, value])

        return result

    def action_trace_data(self):
        """
        :return:
        """
        if not self.__slow_action:
            return []

        return {"type": "actionTraceData", "actionTraces": [value for value in six.itervalues(self.__slow_action)]}

    def slow_sql_data(self):
        """
        :return:
        """
        if not self.__slow_sql_stats:
            return []

        result = {"type": "sqlTraceData", "sqlTraces": []}
        maximum = self.__settings.slow_sql_count
        slow_sql_nodes = sorted(six.itervalues(self.__slow_sql_stats), key=lambda x: x.max_call_time)[-maximum:]

        for node in slow_sql_nodes:
            explain_plan = node.slow_sql_node.explain_plan
            params = {"explainPlan": explain_plan if explain_plan else {}, "stacktrace": []}

            if node.slow_sql_node.stack_trace:
                for line in node.slow_sql_node.stack_trace:
                    if len(line) >= 4:
                        params['stacktrace'].append("%s(%s:%s)" % (line[2], line[0], line[1]))

            result['sqlTraces'].append([node.slow_sql_node.start_time, node.slow_sql_node.path,
                                        node.slow_sql_node.metric, node.slow_sql_node.request_uri,
                                        node.slow_sql_node.formatted, node.call_count,
                                        node.total_call_time, node.max_call_time,
                                        node.min_call_time, str(params)])

        return result
