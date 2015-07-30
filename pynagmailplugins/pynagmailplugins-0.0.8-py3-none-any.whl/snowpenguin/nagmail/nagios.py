import nagiosplugin

from .postfix import *

class MailQueue(nagiosplugin.Resource):
    name = 'MAILQ'

    def __init__(self, mailq_interface: MailQueueInterface):
        self.mailq_interface = mailq_interface

    def probe(self):
        self.mailq_interface.update()

        if self.mailq_interface.has_total_counter():
            yield nagiosplugin.Metric('total', self.mailq_interface.get_total_counter(), min=0)

        if self.mailq_interface.has_active_counter():
            yield nagiosplugin.Metric('active', self.mailq_interface.get_active_counter(), min=0)

        if self.mailq_interface.has_deferred_counter():
            yield nagiosplugin.Metric('deferred', self.mailq_interface.get_deferred_counter(), min=0)

class MailQueueSummary(nagiosplugin.Summary):
    def __init__(self, contexts):
        self.contexts = contexts

    def ok(self, results):
        first = True
        result = ""
        for c in self.contexts:
            if first:
                first = False
            else:
                result += " - "
            result += "%s: %s" % (c, str(results[c].metric))

        return result


def create_mailq_check(mq_interface, total_warning, total_critical, deferred_warning, deferred_critical):

    check = nagiosplugin.Check(
        MailQueue(mq_interface),
    )

    summary_contexts = []

    if mq_interface.has_total_counter():
        check.add(nagiosplugin.ScalarContext('total', total_warning, total_critical))
        summary_contexts.append('total')

    if mq_interface.has_active_counter():
        check.add(nagiosplugin.ScalarContext('active', total_warning, total_critical))
        summary_contexts.append('active')

    if mq_interface.has_deferred_counter():
        check.add(nagiosplugin.ScalarContext('deferred', deferred_warning, deferred_critical))
        summary_contexts.append('deferred')

    check.add(MailQueueSummary(summary_contexts))

    return check
