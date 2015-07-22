__author__ = 'phg49389'

import json
import multiprocessing as mp
import time

from bu_cascade.cascade_connector import Cascade
from config import WSDL, CASCADE_LOGIN as AUTH, SITE_ID

output = mp.Queue()
cascade = Cascade(WSDL, AUTH, SITE_ID)

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

# This method, once finished, will construct an asset, then have Cascade either create it or edit it appropriately.
# Still need to finish the methods below before this one will work.
def submit_form(form_contents, submit_new):
    storage = cascade.dynamo.storage
    data = [(elem.split("=", 1)[0], elem.split("=", 1)[1]) for elem in form_contents.split("`")]
    data_structure = recursively_create_structure_for_data_nodes(data)
    structured_data_nodes = turn_data_structure_into_nodes(data_structure)

    asset = {
        'page': {
            'name': storage[0],
            'siteId': storage[1],
            'parentFolderPath': storage[2],
            'metadataSetPath': storage[3],
            'contentTypePath': storage[4],
            'configurationSetPath': storage[5],
            'structuredData': structured_data_nodes,
            'metadata': storage[6]
        },
        'workflowConfiguration': storage[7]
    }

    print asset

    if submit_new:
        # cascade.create(asset)
        pass
    else:
        # cascade.edit(asset)
        pass

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

