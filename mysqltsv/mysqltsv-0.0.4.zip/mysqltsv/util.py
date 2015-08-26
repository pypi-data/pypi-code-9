import logging

logger = logging.getLogger("mysqltsv.util")

def encode(val, none_string="NULL"):
    if val == None:
        return none_string
    elif isinstance(val, bytes):
        val = str(val, 'utf-8', "replace")
    else:
        val = str(val)

    return val.replace("\t", "\\t").replace("\n", "\\n")


def decode(val, type=str, none_string="NULL"):
    if val == none_string:
        return None
    else:
        if isinstance(val, bytes):
            val = str(val, 'utf-8', "replace")

    return type(val.replace("\\t", "\t").replace("\\n", "\n"))

def read_row(line, *args, types=None, **kwargs):
    raw_values = line.strip("\n").split("\t")

    if types is None:
        return (decode(rv, *args, **kwargs) for rv in raw_values)
    else:
        return (decode(rv, *args, type=t, **kwargs)
                for rv, t in zip(raw_values, types))


def write_row(row, f, *args, headers=None, **kwargs):

    if isinstance(row, dict):
        if headers is None:
            raise ValueError("Cannot write `dict` without specifying headers.")

        values = [row[h] for h in headers]
    elif hasattr(row, 'values'):
        # Probably one of our abstract row types
        values = list(row.values())
    elif hasattr(row, "__iter__"):
        values = list(row)
    else:
        raise ValueError("row is non-iterable type {0}".format(type(row)))

    f.write("\t".join(encode(v, *args, **kwargs) for v in values))
    f.write("\n")
