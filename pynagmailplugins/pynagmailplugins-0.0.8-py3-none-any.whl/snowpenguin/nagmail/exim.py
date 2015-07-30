import io
import subprocess

from .common import MailQueueInterface, MailQueueDataFetchError

class EximMailQueue(MailQueueInterface):
    def __init__(self, data_generator):
        super(EximMailQueue, self).__init__(data_generator)
        self.total = 0

    def has_deferred_counter(self):
        return False

    def get_deferred_counter(self):
        return 0

    def has_active_counter(self):
        return False

    def get_active_counter(self):
        return 0

    def has_total_counter(self):
        return True

    def get_total_counter(self):
        return self.total

    def update(self):

        mailq_output = self.data_generator()

        if mailq_output is None:
            return

        for line in mailq_output:
            try:
                self.total = int(line)
                break
            except ValueError as e:
                raise MailQueueDataFetchError(e)

MailQueueInterface.register(EximMailQueue)

class EximMailqFetcher:
    def __init__(self, use_sudo=False):
        self.sudo = use_sudo

    def get_data(self):

        popen_target = ['sudo', 'mailq', '-bpc'] if self.sudo else ['mailq', '-bpc']

        try:

            p = subprocess.Popen(popen_target,
                                 stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            pres, err = p.communicate()
        except FileNotFoundError as e:
            raise MailQueueDataFetchError(e)

        if err:
            raise MailQueueDataFetchError(err)

        if pres:
            return io.StringIO(pres.decode('utf-8'))
