"""Parse lab parameter files"""


def read_atom_param(filepath):
    with open(filepath, "r") as f:
        return read_atom_param_stream(f)


def read_atom_param_stream(stream):
    params = {
        'version': None,
        'atoms': {},
        'pwpot': {}
    }

    for l in iter(stream):
        ss = l.strip().split()
        if ss:
            rec_type = ss[0]

            if rec_type == "version":
                params['version'] = ss[1]
            if rec_type == "atom":
                major, minor = ss[2], ss[3]
                pwpot_id = ss[4]
                radius = float(ss[5])
                charge = float(ss[6])

                params['atoms'][(major, minor)] = {}

    return params
