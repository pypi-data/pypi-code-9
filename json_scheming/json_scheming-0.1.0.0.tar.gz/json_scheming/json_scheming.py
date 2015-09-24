'''Just a bunch of pure-python functions for dealing with nested
lists and dictionaries from a typical json file

BIG CAVEATS:
* Expects a top-level list
* Does not allow lists nested directly in other lists
  (lists should only contain dictionaries or leaves)

This may change with future developments :)
'''

try:
    import simplejson as json
except ImportError:
    import json

def get_first_non_empty_value(x):
    for i in x:
        if i is not None:
            return i
    
    return None

def check_if_all_same(x):
    x0= x[0]
    return all([i==x0 for i in x])

def get_all_keys(ld):
    return list(set.union(*[set(i.keys()) for i in ld if i is not None]))

def rotate_list_of_dicts(ld):
    '''Change from a list of dicts to a dict of lists
       Fill missing entries with "None"
       This is not very efficient, but it works.'''
    return {k: [(None if i is None or k not in i else
                 i[k])
                for i in ld]
            for k in get_all_keys(ld)}

def flatten(x):
    '''Flatten a list of lists'''
    return [j for i in x
              if i is not None
              for j in i]

def dict_apply(f, d):
    return {k: f(v) for k, v in d.iteritems()}

def build_summary(l):
    '''Return summary information about a list:
       * Does list contain empty values (None's)?
       * Are all entries the same?
       * What is the first actual value?
       * Are any elements lists?
       * Are any elements dicts?
       * {Nested details...}
    '''
    has_empty = None in l
    has_all_same = check_if_all_same(l)
    has_lists = any(type(i) == list for i in l)
    has_dicts = any(type(i) == dict for i in l)    
    fail_str = 'Mixed dicts and lists, no recursion is possible'
    first_val = get_first_non_empty_value(l)
    nested_details = (fail_str if has_lists and has_dicts else
                      build_summary(flatten(l)) if has_lists else
                      dict_apply(build_summary, rotate_list_of_dicts(l)) if has_dicts else
                      ('SAMPLEVALUE:', first_val)
                     )
    
    #if has_dicts: # TESTING
    #    print dict_apply(build_summary, rotate_list_of_dicts(l))
    #    BORK
    
    return ('missing' if has_empty else 'complete',
            'uniform' if has_all_same else 'varying',
            'list' if has_lists else 'dict' if has_dicts else 'leaf',
            nested_details,
           )

def summarize_list_of_dicts(ld):
    return dict_apply(build_summary, rotate_list_of_dicts(ld))

def get_attr_str(v):
    return '(' + ' | '.join(map(str, v[:-1])) + ')'

def recursive_build_schema_summary(summary_dict, depth=0, join_strings=True):
    out_strs = []
    indent = '    ' * depth
    for k, v in summary_dict.iteritems():
        s = indent + str(k) + ':   ' + get_attr_str(v)
        out_strs.append(s)
        
        if type(v[-1]) == dict:
            out_strs += recursive_build_schema_summary(v[-1], depth+1, join_strings=False)
        elif type(v[-1][-1]) == dict:
            s = indent + '    <list>:   ' + get_attr_str(v[-1])
            out_strs.append(s)
            out_strs += recursive_build_schema_summary(v[-1][-1], depth+2, join_strings=False)
        else:
            s = '  ' + '    ' * depth + ' ' + repr(v[-1][-1])
            out_strs.append(s)
    
    return '\n'.join(out_strs) if join_strings else out_strs

def build_schema_from_list_of_dicts(ld):
    return recursive_build_schema_summary(summarize_list_of_dicts(ld))

def load_new_line_delimited_json(f):
    # Load the json to a list of dicts
    j = []
    with open(f) as fid:
        for i in fid:
            j.append(json.loads(i))
    return j

def summarize_new_line_delimited_json(f):
    return build_schema_from_list_of_dicts(
             load_new_line_delimited_json(f)
           )
