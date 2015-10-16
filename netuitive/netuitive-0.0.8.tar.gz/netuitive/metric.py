
class Metric(object):

    """
        A performance measure that is associated with Element

        :param metricId: Metric FQN
        :type metricId: string
        :param metricType: Metric Type
        :type metricType: string
        :param sparseDataStrategy: Sparse data strategy
        :type sparseDataStrategy: string
        :param unit: Metric Unit type
        :type unit: string
    """

    def __init__(self, metricId, metricType=None, sparseDataStrategy='None', unit=''):
        self.id = metricId
        self.type = metricType
        self.sparseDataStrategy = sparseDataStrategy
        self.unit = unit
