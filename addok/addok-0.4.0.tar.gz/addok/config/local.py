# Above this treshold, terms are considered commons.
COMMON_THRESHOLD = 500
LOG_QUERIES = True
LOG_NOT_FOUND = True
EXTRA_FIELDS = [
    {'key': 'citycode'},
]
FILTERS = ["type", "postcode", "citycode", "city"]
INTERSECT_LIMIT = 100
