
import re
from ast import *

def make_print(xs):
  print("print:", xs)
  elts = map(transform_x, xs)
  if len(elts) == 1:
    values = elts[0]
  elif len(elts) == 0:
    values = [Tuple(elts=[], ctx=Load())]
  else:
    values = [Tuple(elts=elts, ctx=Load())]
  return Print(dest=None, values=values, nl=True)

def make_plus(xs):
  pass

def make_apply(xs):
  pass

def transform_xs(xs):
  if len(xs) == 0:
    raise ValueError('xs to transform is empty')
  else:
    head = xs[0]
    if head == 'print':
      return make_print(xs[1:])
    elif head == '+':
      return make_plus(xs[1:])
    else:
      return make_apply(xs[1:])

def transform_token(token):
  if token[0] == ':':
    return Str(token[1:])
  elif re.match("^\\d+$", token):
    return Num(int(token))
  elif re.match("^\\d+(\.\\d+)?$", token):
    return Num(float(token))
  else:
    return Name(id=token, ctx=Load())

def transform_x(x):
  if type(x) == list:
    return transform_xs(x)
  elif type(x) == str:
    return transform_token(x)
  else:
    raise ValueError('unknown type to transform')

def transform(tree):
  return Module(body=map(transform_xs, tree))
