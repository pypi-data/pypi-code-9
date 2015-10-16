
class Sample(object):

    """
        A data point of the Metric
        :param metricId: Metric FQN
        :type metricId: string
        :param timestamp: Timestamp for the sample
        :type timestamp: int
        :param value: Value of the metric
        :type value: float
    """

    def __init__(self, metricId, timestamp, val):
        self.metricId = metricId
        self.timestamp = timestamp
        self.val = val
