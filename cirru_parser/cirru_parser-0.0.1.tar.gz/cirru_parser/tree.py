
def appendItem(xs, level, buffer):
  if level == 0:
    return xs + [buffer]
  else:
    res = appendItem(xs[-1], (level - 1), buffer)
    return xs[:-1] + [res]

def createHelper(xs, n):
  if n <= 1:
    return xs
  else:
    return [createHelper(xs, (n - 1))]

def createNesting(n):
  return createHelper([], n)

def dollbarHelper(before, after):
  if len(after) == 0:
    return before
  cursor = after[0]
  if type(cursor) == list:
    return dollbarHelper(before + [resolveDollar(cursor)], after[1:])
  elif cursor['text'] == '$':
    return before + [resolveDollar(after[1:])]
  else:
    return dollbarHelper(before + [cursor], after[1:])

def resolveDollar(xs):
  if len(xs) == 0:
    return xs
  else:
    return dollbarHelper([], xs)

def commaHelper(before, after):
  if len(after) == 0:
    return before
  cursor = after[0]
  if (type(cursor) == list) and (len(cursor) > 0):
    head = cursor[0]
    if type(head) == list:
      return commaHelper(before + [resolveComma(cursor)], after[1:])
    elif head['text'] == ',':
      return commaHelper(before, resolveComma(cursor[1:]) + after[1:])
    else:
      return commaHelper(before + [resolveComma(cursor)], after[1:])
  else:
    return commaHelper(before + [cursor], after[1:])

def resolveComma(xs):
  if len(xs) == 0:
    return xs
  else:
    return commaHelper([], xs)
