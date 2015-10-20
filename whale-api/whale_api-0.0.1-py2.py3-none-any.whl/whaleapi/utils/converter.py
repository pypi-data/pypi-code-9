import datetime


def epoch_to_iso_8601(seconds_since_epoch):
    time_object = datetime.datetime.utcfromtimestamp(float(seconds_since_epoch))
    return time_object.isoformat() + 'Z'
