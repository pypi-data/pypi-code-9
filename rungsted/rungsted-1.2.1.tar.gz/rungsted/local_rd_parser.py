__author__ = 'anders'

line = "NOUN ?VERB ?NOUN 1.0 'abe| f1:1.0 f2 |b f3:7 f4\n"

i = 0

def read_token(token_type, until=None):
    global i
    start_i = i
    while not (line[i] == "\n" or line[i].isspace() or line[i] == until):
        i += 1

    print("Got token '{}' ({}) {}-{}".format(line[start_i:i], token_type, start_i, i))

    while line[i].isspace() and not line[i] == "\n":
        i += 1

def is_eol():
    return i == len(line) - 1

def labels_rule():
    if line[i].isdigit() or line[i] == '\'':
        return False

    if line[i] == '?':
        label_constraint_rule()
    else:
        label_rule()

    return True


def label_constraint_rule():
    read_token("label_constraint")

def label_rule():
    read_token("label")

def importance_rule():
    if line[i].isdigit():
        read_token("importance_weight")

def id_rule():
    global i
    if line[i] == "'":
        i += 1
        read_token('id', until="|")

def header_rule():
    while labels_rule():
        pass
    importance_rule()
    id_rule()

def feature_rule():
    global i
    if line[i] == '|' or is_eol():
        return False

    read_token('feature_name', ':')

    if line[i] == ':':
        i += 1
        read_token('feature_value')

    return True

def ns_rule():
    if line[i] != '|':
        raise RuntimeError("Expected namespace: " +  line[i:])
    read_token('ns_def')

    while feature_rule():
        pass

    if not is_eol():
        return True


def instance_rule():
    header_rule()
    while ns_rule():
        pass


instance_rule()