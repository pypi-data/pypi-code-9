from whaleapi.api.base import SendableAPIResource


class Metric(SendableAPIResource):
    class_name = 'metric'
    class_url = '/metrics'
    plural_class_name = 'metrics'
    json_name = 'metric'

    @classmethod
    def send(cls, metrics=None, **single_metric):

        if metrics:
            metrics_dict = {"metrics": metrics}
        else:
            metrics = [single_metric]
            metrics_dict = {"metrics": metrics}

        return super(Metric, cls).send(**metrics_dict)
