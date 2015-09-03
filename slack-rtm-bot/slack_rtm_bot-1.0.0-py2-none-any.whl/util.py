def parse_int(query, default=None):
  try:
    return int(query)
  except ValueError:
    return default
