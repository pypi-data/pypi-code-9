__author__ = 'phg49389'

import ast
import re
import json
import multiprocessing as mp
import time

from bu_cascade.cascade_connector import Cascade
from bu_cascade.dynamic_data_def_builder.dynamic_data_def import DataDefinitionBuilder
from config import WSDL, CASCADE_LOGIN as AUTH, SITE_ID

output = mp.Queue()
cascade = Cascade(WSDL, AUTH, SITE_ID)
printer = DataDefinitionBuilder(cascade, "foo")

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
    # print "Submit has been called in interfacer"
    header_data = form_contents[0]
    asset = ast.literal_eval(header_data[1])
    type_of_page = asset.keys()[0]
    form_contents = form_contents[1:]
    data_structure = recursively_create_structure_for_data_nodes(form_contents)
    structured_data_nodes = turn_data_structure_into_nodes(data_structure)
    asset[type_of_page]['structuredData']['structuredDataNodes'] = structured_data_nodes

    printer.pretty_print(asset)
    # print "Submitted"
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
    return { 'structuredDataNode': structured_data }

def structured_data_node(node_id, text_value, node_type=None, children_list=None):
    b_path = None
    f_path = None
    p_path = None
    assetType = None
    if not node_type:
        node_type = "text"
    elif node_type != "group":
        if node_type == "block":
            b_path = text_value
        elif node_type == "file":
            f_path = text_value
        elif node_type == "page":
            p_path = text_value
        assetType = node_type
        text_value = None
        node_type = "asset"

    if children_list:
        children_list = turn_data_structure_into_nodes(children_list)

    to_return = {
        'assetType': assetType,
        'blockPath': b_path,
        'filePath': f_path,
        'identifier': node_id,
        'pagePath': p_path,
        'structuredDataNodes': children_list,
        'text': text_value,
        'type': node_type
    }
    return to_return

################
# Testing code #
################

#########################
# Here's the plan:
# 1. On submission, pass through the list of tuples
# 2. The first part of the list will contain the metadata fields
# 3. The third part will contain the actual data from the page
# 4. The entry between the two parts will contain a string literal of the dictionary needed for the asset,
#        constructed before the page gets made
#########################

def B_get_event_structure(workflow=None, event_id=None):
    # 1. A list of structured_data_node objects
    structured_data = [
        B_structured_data_node("vimeo-url", "N/A"),
        B_structured_data_node("youtube", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        B_structured_data_node("caption", "You got RickRolled!")
    ]

    # Wrap in the required structure for SOAP
    structured_data = {
        'structuredDataNodes': {
            'structuredDataNode': structured_data,
        },
        # 2. The ID of the data definition being used for this data
        'definitionId': "ba13cf948c586513100ee2a733d00a0b"
    }

    # 3. A list of dynamic_fields?
    dynamic_fields = {
        'dynamicField': [
            B_dynamic_field('department', ["Math & Computer Science"]),
            B_dynamic_field('degree', ["Bachelor of Science"]),
            B_dynamic_field('school', ["College of Arts & Sciences"]),
            B_dynamic_field('program-type', ["Major"]),
        ],
    }

    asset = {
        'xhtmlDataDefinitionBlock': { # 4. Is it a page or block?
            'siteId': "ba134ac58c586513100ee2a7cec27f4a",  # Should be able to extract from Tinker's app
            'id': "3cff91f18c58651314811f9cf2a10e7f",  # 5. The id of the block/page being edited
            'name': "dd-editor-simple-test", # 6.
            'path': "_testing/philip-gibbens/dynamic-dd-editor-tests/dd-editor-simple-test",
            'parentFolderPath': "_testing/philip-gibbens/dynamic-dd-editor-tests",
            'structuredData': structured_data,
            'metadata': {
                'title': "Duckroll",
                'summary': 'summary',
                'author': "phg49389",
                'dynamicFields': dynamic_fields,
            }
        }
    }

    if event_id:
        asset['page']['id'] = event_id

    return asset

def B_structured_data_node(node_id, text, node_type=None):

    if not node_type:
        node_type = "text"

    node = {

        'identifier': node_id,
        'text': text,
        'type': node_type,
    }

    return node

def B_dynamic_field(name, values):

    values_list = []
    for value in values:
        values_list.append({'value': value})
    node = {
        'name': name,
        'fieldValues': {
            'fieldValue': values_list,
        },
    }

    return node
