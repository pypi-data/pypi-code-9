import os
import collections
import copy


def get_section(keyword, stt_file=None, data=None):
    if stt_file:
        with open(stt_file, 'r') as f:
            data = f.readlines()
            return _get_section(keyword, data)
    elif data:
        return _get_section(keyword, data)


def _get_section(keyword, data):
    sections = []
    reading = False
    for line in data:
        if "END" + keyword in line:
            section.append(line)
            sections.append(section)
            reading = False
        elif keyword in line:
            reading = True
            section = []
        if reading:
            section.append(line)
    return sections


def remove_section(keyword, stt_file=None, data=None):
    if stt_file:
        with open(stt_file, 'r') as f:
            data = f.readlines()
            with open(stt_file, 'w') as f:
                f.writelines(_remove_section(keyword, data))
    elif data:
        return _remove_section(keyword, data)


def _remove_section(keyword, data):
    stt_data = []
    reading = True
    for line in data:
        if reading and keyword not in line:
            stt_data.append(line)
        if "END" + keyword in line:
            reading = True
        elif keyword in line:
            reading = False
    return stt_data


def add_section(raw, stt_file):
    with open(stt_file, 'r') as f:
        stt_data = f.readlines()
    with open(stt_file, 'w') as g:
        g.writelines(stt_data)
        g.writelines(raw)


def get_attribute_value(row, keyword):
    name = ""
    for line in row:
        key = line.lstrip().split(" ")[0]
        if keyword == key:
            name = line.split(" ")[-1].rstrip('\n')
    return name


def change_attribute_value(key, value, data):
    for i in range(len(data)):
        keyword = data[i].lstrip().split(" ")[0]
        if keyword == key:
            data[i] = keyword + " " + str(value) + os.linesep
    return data


def remove_section_headers(data):
    for d in data:
        first = d[0]
        stop = d[-1]
        if "END" + first.split()[0] != stop.split()[0]:
            print "error in remove section headers, headers do not match"
        d.remove(first)
        d.remove(stop)
    return data


def extract_attribute(data):
    attributes = collections.OrderedDict()
    for d in data:
        a = d.split()
        if len(a) > 1:
            attributes[a[0]] = " ".join(a[1:])

    return attributes


def extract_file(data):
    stt_data = {}
    stt_data = extract_attribute(data)
    stt_data['filename'] = data[0].split()[1]
    return stt_data


def parser(stt_file):
    sections = {"BBMR": {},
                "USERDEFREF": {},
                "BCMB": {"ROW": {"CORE": {}}},
                "SURFACE_TREE": {"SURFACE": {}},
                "CAD": {}}  # ,
    # "FILE": []}
    with open(stt_file, 'r') as f:
        lines = f.readlines()
        return auto_parser(lines)


def dict2array(data):
    res = []
    for key in data.keys():
        if isinstance(data[key], list):
            for d in data[key]:
                sub = dict2array(d)
                sub = add_section_headers(sub, key)
                res += sub

        elif isinstance(data[key], dict):
            sub = dict2array(data[key])
            sub = add_section_headers(sub, key)
            res += sub
        else:
            res.append(key + " " + str(data[key]) + "\n")
    return res


def add_section_headers(data, section, extra=""):
    if section != "grids":
        data.insert(0, section + " " + extra + "\n")
        data.append("END" + section + "\n")
    return data


def remove_filename_from_file(data):
    data_2 = copy.deepcopy(data)
    filename = data['filename']
    del data_2['filename']
    return filename, data_2


def write_section(section, section_data, stt_file):
    if isinstance(section_data, list):
        remove_section(section, stt_file=stt_file)
        for sec in section_data:
            write_section(section, sec, stt_file)
    else:
        if section != "FILE":
            remove_section(section, stt_file=stt_file)

        extra = ""
        if section == "FILE":
            extra, section_data = remove_filename_from_file(section_data)
        data = dict2array(section_data)
        data = add_section_headers(data, section, extra)
        add_section(data, stt_file=stt_file)


def find_all_sections(data):
    sections = []
    for line in data:
        if line.strip().startswith("END"):
            sections.append(line.strip()[3:])
    return list(set(sections))


def find_first_section_occurence(lines, sections):
    for line in lines:
        name = line.strip().split()
        if len(name) > 0 and name[0] in sections:
            return name[0]
    return "", ""


def bbmr_parser(lines):
    data = collections.OrderedDict()
    grids, lines = get_grid_sections_and_remove(lines)
    data = extract_attribute(lines)
    data['grids'] = []
    for grid in grids:
        data['grids'].append(extract_attribute(grid))
    return data


def get_grid_sections_and_remove(lines):
    grids = []
    grid = []
    reading = False
    new_lines = []
    for line in lines:
        if "grid" in line:
            reading = True
            if grid != []:
                grids.append(grid)
            grid = []
        if reading:
            grid.append(line)
        else:
            new_lines.append(line)

    if grid != []:
        grids.append(grid)
    return grids, new_lines


def remove_grid_sections(lines):
    return lines


def auto_parser(lines):
    data = collections.OrderedDict()
    sections = find_all_sections(lines)
    while len(sections) > 0:
        section = find_first_section_occurence(lines, sections)
        section_lines = get_section(section, data=lines)

        if section == "FILE":
            for section_line in section_lines:
                to_write = "filename " + section_line[0].split()[1]
                section_line.insert(1, to_write)

        section_lines = remove_section_headers(section_lines)

        if section == "BBMR":
            data[section] = bbmr_parser(section_lines[0])

        elif len(section_lines) > 1:
            data[section] = []
            for section_line in section_lines:
                data[section].append(auto_parser(section_line))
        else:
            data[section] = auto_parser(section_lines[0])
        lines = remove_section(section, data=lines)
        sections = find_all_sections(lines)

    data = collections.OrderedDict(extract_attribute(lines).items() + data.items())
    return data


