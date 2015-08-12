__author__ = 'phg49389'

import re
import json
import multiprocessing as mp
import time

from bu_cascade.cascade_connector import Cascade
# from bu_cascade.dynamic_data_def_builder.dynamic_data_def import DataDefinitionBuilder
from config import WSDL, CASCADE_LOGIN as AUTH, SITE_ID

output = mp.Queue()
cascade = Cascade(WSDL, AUTH, SITE_ID)
# printer = DataDefinitionBuilder(cascade, "foo")

def fetch_array(user_name, called=""):
    print "fetch_array called!"
    start = time.time()
    called = "/" + called
    array = ["folder~" + called]

    storage = cascade.read(called, "folder")['asset']
    if storage['folder']['children'] is not None:
        storage = storage['folder']['children']['child']
    else:
        return json.dumps([])

    # Get the relevant credentials
    try:
        user = cascade.client.service.read(cascade.login, {'id': user_name, 'type': "user"})
        allowed_groups = user.asset.user.groups
    except AttributeError:
        allowed_groups = ""
    user_groups = allowed_groups.split(";")

    processes = [
        mp.Process(target=read_access_rights, args=(item['id'], item['type'], output, storage.index(item)))
        for item in storage]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes and get results
    result_storage = []
    for p in processes:
        p.join(1)  # Typically takes less than a second, so have a timeout in case of errors
        while not output.empty():
            result_storage.append(output.get())
        if p.is_alive():
            print str(processes.index(p)) + " is still alive"
            p.terminate()
            print "This process is still alive: ", p.is_alive()

    # Because multiprocesses don't return in order ran, the results need to be sorted.
    # That's why the index of the item having its permission inspected is necessary as an arg
    results = [result[1] for result in sorted(result_storage, key=lambda x: x[0])]

    for item in storage:
        # Each result should be a list of all approved individual users and groups
        result = results[storage.index(item)]
        if user_name in result or set(user_groups).intersection(set(result)):
            # item = storage[results.index(result)]
            array.append(item['type'] + "~" + item['path']['path'].split("/")[-1])

    print str(len(array)) + " items being returned by fetch"
    end = time.time()
    print str(end - start) + " seconds"
    return json.dumps(array)

def read_access_rights(page_id, page_type, q, index):
    identifier = {
        'id': page_id,
        'type': page_type,
    }
    response = cascade.client.service.readAccessRights(cascade.login, identifier)['accessRightsInformation']['aclEntries']['aclEntry']
    to_return = [right['name'] for right in response]
    q.put((index, to_return))

# This method will construct an asset, then have Cascade either create it or edit it appropriately.
def submit_form(form_contents, submit_new):
    print "Submit has been called in interfacer"
    end_of_metadata_index = form_contents.index(("end-of-metadata", "Quoth the raven, nevermore."))
    header_data = form_contents[:end_of_metadata_index]
    page = {}
    for meta_datum in header_data:
        key = str(meta_datum[0])[5:]
        value = str(meta_datum[1]).replace('`', '\"').replace('~', '=')
        if key == "metadata":
            value = convert_metadata_string_to_dict(value)
        page[key] = value
    form_contents = form_contents[end_of_metadata_index+1:]
    data_structure = recursively_create_structure_for_data_nodes(form_contents)
    structured_data_nodes = turn_data_structure_into_nodes(data_structure)
    page['structuredData'] = structured_data_nodes

    asset = {
        'page': page
    }
    print "Submitted"
    if submit_new:
        return cascade.create(asset)
    else:
        return cascade.edit(asset)

def recursively_create_structure_for_data_nodes(unstructured_data):
    to_return = []
    group = []
    inside_group = False
    group_counter = 0  # Will count the depth of groups being nested
    for datum in unstructured_data:
        if "group_" in datum[0]:
            if datum[0] != "group_close":
                if not inside_group:
                    inside_group = True
                    to_return.append(datum)
                else:
                    group.append(datum)
                group_counter += 1
            else:
                group_counter -= 1
                if group_counter == 0:
                    to_return.append(recursively_create_structure_for_data_nodes(group))
                    group = []
                    inside_group = False
                else:
                    group.append(datum)
        else:
            if inside_group:
                group.append(datum)
            else:
                to_return.append(datum)
    return to_return

def turn_data_structure_into_nodes(data_structure):
    # print "Beginning build of structuredDataNodes; there are", len(data_structure), "elements"
    structured_data = []
    for i in range(len(data_structure)):
        if isinstance(data_structure[i], tuple):  # Either element or group header; either way make a new node
            # print data_structure[i]
            if "group_" in data_structure[i][0]:
                # It's a group; grab next element; will be a list with this group's children in it
                ident = data_structure[i][0][6:]
                foo = structured_data_node(ident, data_structure[i][1], "group", data_structure[i+1])
            else:
                # It's data; make a structured data node with no children and add it on to the list we have
                # print data_structure[i]
                if "asset_" in data_structure[i][0]:
                    type_letter = data_structure[i][0][6]
                    type_of_asset = None
                    if type_letter == "p":
                        type_of_asset = "page"
                    elif type_letter == "f":
                        type_of_asset = "file"
                    elif type_letter == "b":
                        type_of_asset = "block"
                    ident = data_structure[i][0][8:]
                    foo = structured_data_node(ident, data_structure[i][1], type_of_asset)
                else:
                    foo = structured_data_node(data_structure[i][0], data_structure[i][1])
            structured_data.append(foo)
        # Ignore the lists, as they'll be grabbed by the groups
    return structured_data

def structured_data_node(node_id, text_value, node_type=None, children_list=None):
    b_path = None
    f_path = None
    p_path = None
    if not node_type:
        node_type = "text"
    else:
        if node_type == "block":
            b_path = text_value
            text_value = None
        elif node_type == "file":
            f_path = text_value
            text_value = None
        elif node_type == "page":
            p_path = text_value
            text_value = None

    if children_list:
        children_list = turn_data_structure_into_nodes(children_list)

    to_return = {
        'assetType': None,
        'blockId': None,
        'blockPath': b_path,
        'fileId': None,
        'filePath': f_path,
        'identifier': node_id,
        'pageId': None,
        'pagePath': p_path,
        'recycled': False,
        'structuredDataNodes': children_list,
        'symlinkId': None,
        'symlinkPath': None,
        'text': text_value,
        'type': node_type
    }
    return to_return

def convert_metadata_string_to_dict(metadata):
    metadata = re.sub("\([^\)]*\)", "", metadata)
    # Removing these padding spaces makes it easier to parse
    metadata = metadata.replace(" = ", "=").replace("{ ", "{").replace(" }", "}").replace(", ", ",")
    # print "Metadata is now: " + metadata
    # print
    to_return = recursively_build_dict_from_metadata_string(metadata[1:-1])
    # printer.pretty_print(to_return)
    return to_return

def recursively_build_dict_from_metadata_string(metadata):
    to_return = {}
    name = ""
    gathering_array = False
    array_being_gathered = []
    current = metadata
    while True:
        returned = get_next_parseable_chunk(current)
        if returned is None:
            break
        if len(returned) == 1:  # A quote-enclosed String
            to_return[name] = returned[0]
            current = ""
        else:
            if returned[1] == "=":
                name = returned[0]
                if "[]" in name:
                    gathering_array = True
                    name = name[:-2]
                current = returned[2]
            elif returned[1] == " ":
                if gathering_array:
                    array_being_gathered.append(recursively_build_dict_from_metadata_string(returned[0]))
                else:
                    to_return[name] = returned[0]
                current = returned[2]
            else:
                if gathering_array:
                    array_being_gathered.append(recursively_build_dict_from_metadata_string(returned[1]))
                else:
                    to_return[name] = recursively_build_dict_from_metadata_string(returned[1])
                current = returned[2]
    if gathering_array:
        to_return[name] = array_being_gathered
    return to_return

def get_next_parseable_chunk(metadata):
    if len(metadata) == 0:
        return None
    chars_to_look_for = ["{", "=", " ", "\""]
    break_flag = True
    for desired_char in chars_to_look_for:
        if desired_char in metadata:
            break_flag = False
    if break_flag:
        return [metadata]
    index = 0
    for char in metadata:
        if char in chars_to_look_for:
            if char == "{":
                index += 1
                brace_pair_counter = 1
                end_index = index + 1
                for other_char in metadata[index+1:]:
                    end_index += 1
                    if other_char == "{":
                        brace_pair_counter += 1
                    elif other_char == "}":
                        brace_pair_counter -= 1
                        if brace_pair_counter == 0:
                            break
                return [metadata[:index], metadata[index:end_index-1], metadata[end_index+1:]]
            elif char == "\"":
                return [metadata]
            elif char == " " or char == "=":
                return [metadata[:index], char, metadata[index+1:]]
        index += 1

