import json


def iso_8601(datetime):
    if datetime is None:
        return datetime
    value = datetime.isoformat()
    if value.endswith('+00:00'):
        value = value[:-6] + 'Z'
    return value


def get_log_entry_data(entry):
    return {
        'date_created': iso_8601(entry.date_created),
        'creator': entry.creator.email,
        'operation': entry.operation,
        'operation_label': entry.get_operation_display(),
        'data': json.loads(entry.data),
    }
