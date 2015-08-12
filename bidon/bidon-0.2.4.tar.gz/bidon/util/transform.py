import bidon.json_patch as JP
from bidon.util import flatten_dict


def get_val(source, extract=None, transform=None):
  if extract is None:
    raw_value = source
  else:
    raw_value = extract(source)

  if transform is None:
    return raw_value
  else:
    return transform(raw_value)


def get_obj(source, extract=None, child_transform=None, transform=None):
  if extract is None:
    obj = source
  else:
    obj = extract(source)

  if child_transform is None:
    data = obj
  else:
    # data = {k: v(obj) for k, v in child_transform.items()}
    data = dict()
    for k, v in child_transform.items():
      try:
        data[k] = v(obj)
      except Exception as ex:
        raise Exception("An error occurred with child {0}".format(k)) from ex

  if transform is None:
    return data
  else:
    return transform(data)


def get_lst(source, extract=None, transform=None):
  if extract is None:
    raw_list = source
  else:
    raw_list = extract(source)

  if transform is None:
    return raw_list
  else:
    # return [transform(item) for item in raw_list]
    tlist = []
    for idx, item in enumerate(raw_list):
      try:
        tlist.append(transform(item))
      except Exception as ex:
        raise Exception("An error occurred with item #{0}".format(idx)) from ex
    return tlist


def get_composition(source, *fxns):
  val = source
  for fxn in fxns:
    val = fxn(val)
  return val


def get_flattened(dct, names, path_joiner="_"):
  new_dct = dict()
  for key, val in dct.items():
    if key in names:
      child = {path_joiner.join(k): v for k, v in flatten_dict(val, (key, ))}
      new_dct.update(child)
    else:
      new_dct[key] = dct[key]
  return new_dct


def val(extract=None, transform=None):
  return lambda source: get_val(source, extract, transform)


def obj(extract=None, child_transform=None, transform=None):
  return lambda source: get_obj(source, extract, child_transform, transform)


def lst(extract=None, transform=None):
  return lambda source: get_lst(source, extract, transform)


def compose(*fxns):
  return lambda source: get_composition(source, *fxns)


def flatten(names, path_joiner="_"):
  return lambda dct: get_flattened(dct, names, path_joiner)


def get_xml_attr(source, name, path=None):
  if path is None:
    return source.attrib[name]
  else:
    return get_xml_attr(get_xml_child(source, path), name)


def get_xml_text(source, path=None):
  if path is None:
    return source.text
  else:
    return get_xml_text(get_xml_child(source, path))


def get_xml_child(source, path):
  return source.find(path)


def get_xml_children(source, path):
  return source.findall(path)


def xml_attr(name, path=None):
  return lambda source: get_xml_attr(source, name, path)


def xml_text(path=None):
  return lambda source: get_xml_text(source, path)


def xml_child(path):
  return lambda source: get_xml_child(source, path)


def xml_children(path):
  return lambda source: get_xml_children(source, path)


def get_json_val(source, path, *, ignore_bad_path=False):
  try:
    return JP.find(source, path)
  except JP.JsonPathError as ex:
    if ignore_bad_path:
      return None
    else:
      raise


def get_json_vals(source, path):
  yield from JP.find_all(source, path)


def json_val(path, *, ignore_bad_path=False):
  return lambda source: get_json_val(source, path, ignore_bad_path=ignore_bad_path)


def json_vals(path):
  return lambda source: get_json_vals(source, path)
