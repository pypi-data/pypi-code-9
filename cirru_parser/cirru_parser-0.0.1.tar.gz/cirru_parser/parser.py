
import tree

def parse(code, filename):
  buf = None
  state = {
    'name': 'indent',
    'x': 1,
    'y': 1,
    'level': 1,
    'indent': 0,
    'indented': 0,
    'nest': 0,
    'path': filename
  }
  xs = []
  while len(code) > 0:
    result = parsing(xs, buf, state, code)
    [xs, buf, state, code] = result
  res = parsing(xs, buf, state, code)
  res = tree.resolveDollar(res)
  res = tree.resolveComma(res)
  return res

def shorten(xs):
  # print('shorten', xs)
  if type(xs) == list:
    return map(shorten, xs)
  else:
    return xs['text']

def pare(code, filename):
  res = parse(code, filename)
  return shorten(res)

def escape_eof(xs, buf, state, code):
  raise ValueError("EOF in escape state")

def string_eof(xs, buf, state, code):
  raise ValueError("EOF in string state")

def space_eof(xs, buf, state, code):
  return xs

def token_eof(xs, buf, state, code):
  buf['ex'] = state['x']
  buf['ey'] = state['y']
  xs = tree.appendItem(xs, state['level'], buf)
  buf = None
  return xs

def indent_eof(xs, buf, state, code):
  return xs

# escape

def escape_newline(xs, buf, state, code):
  raise ValueError('newline whle escape')

def escape_n(xs, buf, state, code):
  state['x'] += 1
  buf['text'] += '\n'
  state['name'] = 'string'
  return (xs, buf, state, code[1:])

def escape_t(xs, buf, state, code):
  state['x'] += 1
  buf['text'] += '\t'
  state['name'] = 'string'
  return (xs, buf, state, code[1:])

def escape_else(xs, buf, state, code):
  state['x'] += 1
  buf['text'] += code[0]
  state['name'] = 'string'
  return (xs, buf, state, code[1:])

# string

def string_backslash(xs, buf, state, code):
  state['name'] = 'escape'
  state['x'] += 1
  return (xs, buf, state, code[1:])

def string_newline(xs, buf, state, code):
  raise ValueError('newline in a string')

def string_quote(xs, buf, state, code):
  state['name'] = 'token'
  state['x'] += 1
  return (xs, buf, state, code[1:])

def string_else(xs, buf, state, code):
  state['x'] += 1
  buf['text'] += code[0]
  return (xs, buf, state, code[1:])

# space

def space_space(xs, buf, state, code):
  state['x'] += 1
  return (xs, buf, state, code[1:])

def space_newline(xs, buf, state, code):
  if state['nest'] != 0:
    raise ValueError('incorrect nesting')
  state['name'] = 'indent'
  state['x'] = 1
  state['y'] += 1
  state['indented'] = 0
  return (xs, buf, state, code[1:])

def space_open(xs, buf, state, code):
  nesting = tree.createNesting(1)
  xs = tree.appendItem(xs, state['level'], nesting)
  state['nest'] += 1
  state['level'] += 1
  state['x'] += 1
  return (xs, buf, state, code[1:])

def space_close(xs, buf, state, code):
  state['nest'] -= 1
  state['level'] -= 1
  if state['nest'] < 0:
    raise ValueError('close at space')
  state['x'] += 1
  return (xs, buf, state, code[1:])

def space_quote(xs, buf, state, code):
  state['name'] = 'string'
  buf = {
    'text': '',
    'x': state['x'],
    'y': state['y'],
    'path': state['path']
  }
  state['x'] += 1
  return (xs, buf, state, code[1:])

def space_else(xs, buf, state, code):
  state['name'] = 'token'
  buf = {
    'text': code[0],
    'x': state['x'],
    'y': state['y'],
    'path': state['path']
  }
  state['x'] += 1
  return (xs, buf, state, code[1:])

# token

def token_space(xs, buf, state, code):
  state['name'] = 'space'
  buf['ex'] = state['x']
  buf['ey'] = state['y']
  xs = tree.appendItem(xs, state['level'], buf)
  state['x'] += 1
  buf = None
  return (xs, buf, state, code[1:])

def token_newline(xs, buf, state, code):
  state['name'] = 'indent'
  buf['ex'] = state['x']
  buf['ey'] = state['y']
  xs = tree.appendItem(xs, state['level'], buf)
  state['indented'] = 0
  state['x'] = 1
  state['y'] += 1
  buf = None
  return (xs, buf, state, code[1:])

def token_open(xs, buf, state, code):
  raise ValueError('open parenthesis in token')

def token_close(xs, buf, state, code):
  state['name'] = 'space'
  buf['ex'] = state['x']
  buf['ey'] = state['y']
  xs = tree.appendItem(xs, state['level'], buf)
  buf = None
  return (xs, buf, state, code)

def token_quote(xs, buf, state, code):
  state['name'] = 'string'
  state['x'] += 1
  return (xs, buf, state, code[1:])

def token_else(xs, buf, state, code):
  buf['text'] += code[0]
  state['x'] += 1
  return (xs, buf, state, code[1:])

# indent

def indent_space(xs, buf, state, code):
  state['indented'] += 1
  state['x'] += 1
  return (xs, buf, state, code[1:])

def indent_newilne(xs, buf, state, code):
  state['x'] = 1
  state['y'] += 1
  state['indented'] = 0
  return (xs, buf, state, code[1:])

def indent_close(xs, buf, state, code):
  raise ValueError('close parenthesis at indent')

def indent_else(xs, buf, state, code):
  state['name'] = 'space'
  if (state['indented'] % 2) == 1:
    raise ValueError('odd indentation')
  indented = state['indented'] / 2
  diff = indented - state['indent']

  if diff <= 0:
    nesting = tree.createNesting(1)
    xs = tree.appendItem(xs, (state['level'] + diff - 1), nesting)
  elif diff > 0:
    nesting = tree.createNesting(diff)
    xs = tree.appendItem(xs, state['level'], nesting)

  state['level'] += diff
  state['indent'] = indented
  return (xs, buf, state, code)

# parse

def parsing(*args):
  [xs, buf, state, code] = args
  # print('\nparsing:')
  # print('xs:', xs)
  # print('buf:', buf)
  # print('state:', state)
  # print('code:', code)
  eof = len(code) == 0
  if eof:
    char = None
  else:
    char = code[0]
  if state['name'] == 'escape':
    if eof:
      return escape_eof(*args)
    else:
      if char == '\n':
        return escape_newline(*args)
      elif char == 'n':
        return escape_n(*args)
      elif char == 't':
        return escape_t(*args)
      else:
        return escape_else(*args)
  elif state['name'] == 'string':
    if eof:
      return string_eof(*args)
    else:
      if char == '\\':
        return string_backslash(*args)
      elif char == '\n':
        return string_newline(*args)
      elif char == '"' :
        return string_quote(*args)
      else:
        return string_else(*args)
  elif state['name'] == 'space':
    if eof:
      return space_eof(*args)
    else:
      if char == ' ':
        return space_space(*args)
      elif char == '\n':
        return space_newline(*args)
      elif char == '(':
        return space_open(*args)
      elif char == ')':
        return space_close(*args)
      elif char == '"':
        return space_quote(*args)
      else:
        return space_else(*args)
  elif state['name'] == 'token':
    if eof:
      return token_eof(*args)
    else:
      if char == ' ':
        return token_space(*args)
      elif char == '\n':
        return token_newline(*args)
      elif char == '(':
        return token_open(*args)
      elif char == ')':
        return token_close(*args)
      elif char == '"' :
        return token_quote(*args)
      else:
        return token_else(*args)
  elif state['name'] == 'indent':
    if eof:
      return indent_eof(*args)
    else:
      if char == ' ':
        return indent_space(*args)
      elif char == '\n':
        return indent_newilne(*args)
      elif char == ')':
        return indent_close(*args)
      else:
        return indent_else(*args)
  else:
    raise ValueError('unknown state')
