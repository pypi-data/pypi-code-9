__author__ = 'phg49389'

import ast
import json
import multiprocessing as mp
import re
import time

from bu_cascade.cascade_connector import Cascade
from bu_cascade.dynamic_data_def_builder.dynamic_data_def import DataDefinitionBuilder
from config import WSDL, CASCADE_LOGIN as AUTH, SITE_ID

output = mp.Queue()
cascade = Cascade(WSDL, AUTH, SITE_ID)
printer = DataDefinitionBuilder(cascade, "foo")


# This method exists so that the modal menu for choosing an asset in the HTML editor will work. It bridges the HTML
# to Cascade and checks to see if that user and their groups has access to the individual contents, then returns.
def fetch_array(user_name, called=""):
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


# This method gets the access rights from each item in the folder, and returns them to fetch_array for checking against
# the user and their groups.
def read_access_rights(page_id, page_type, q, index):
    identifier = {
        'id': page_id,
        'type': page_type,
    }
    response = cascade.client.service.readAccessRights(cascade.login, identifier)['accessRightsInformation'][
        'aclEntries']['aclEntry']
    to_return = [right['name'] for right in response]
    q.put((index, to_return))


# This method takes in a flat list of tuples, and then either builds a new asset to submit to Cascade, or builds a new
# asset to submit
def submit_form(form_contents, submit_new):
    header_data = form_contents[0]
    asset = ast.literal_eval(header_data[1])
    if submit_new:
        new_path = form_contents[-2][1]
        new_name = form_contents[-1][1]
        type_of_page = 'xhtmlDataDefinitionBlock'
        # if asset['dataDefinition']['parentContainerPath'] == "Blocks":
        #     type_of_page = 'xhtmlDataDefinitionBlock'
        asset = {
            type_of_page: {
                'name': new_name,
                'siteId': asset['dataDefinition']['siteId'],
                'parentFolderPath': new_path,
                # 'metadata': {
                #     'title': add_data['title'],
                #     'summary': 'summary',
                #     'author': author,
                #     'metaDescription': add_data['teaser'],
                #     'dynamicFields': dynamic_fields,
                # },
                'structuredData': {
                    'definitionId': asset['dataDefinition']['id'],
                    'definitionPath': asset['dataDefinition']['path'],
                    'structuredDataNodes': None
                }
            }
        }
        form_contents = sanitize(form_contents[1:-2])
        data_structure = recursively_create_structure_for_data_nodes(form_contents)
        structured_data_nodes = turn_data_structure_into_nodes(data_structure)
        asset[type_of_page]['structuredData']['structuredDataNodes'] = structured_data_nodes
        printer.pretty_print(asset)
        return cascade.create(asset)
    else:
        type_of_page = asset.keys()[0]
        form_contents = sanitize(form_contents[1:])
        data_structure = recursively_create_structure_for_data_nodes(form_contents)
        structured_data_nodes = turn_data_structure_into_nodes(data_structure)
        asset[type_of_page]['structuredData']['structuredDataNodes'] = structured_data_nodes
        return cascade.edit(asset)


# This method takes the raw data passed from the editor and makes it safe to store in Cascade
def sanitize(list_of_tuples):
    return [(re.sub("(_[0-9]+)*", "", pair[0]), pair[1]) for pair in list_of_tuples]


# This method does exactly what the name suggests; it takes the flat list, and uses the two flags (group_<ident> and
# group_close) to turn it into a usable structure.
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


# This method works in tandem with structured_data_node to take the newly minted structure and turn it into the
# structuredDataNodes that Cascade requires
def turn_data_structure_into_nodes(data_structure):
    structured_data = []
    for i in range(len(data_structure)):
        if isinstance(data_structure[i], tuple):  # Either element or group header; either way make a new node
            if "group_" in data_structure[i][0]:
                # It's a group; grab next element; will be a list with this group's children in it
                ident = data_structure[i][0][6:]
                foo = structured_data_node(ident, data_structure[i][1], "group", data_structure[i + 1])
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
    return {'structuredDataNode': structured_data}


# This method can be thought of as a constructor for a StructuredDataNode, the building block that Cascade uses
def structured_data_node(node_id, text_value, node_type=None, children_list=None):
    b_path = None
    f_path = None
    p_path = None
    asset_type = None
    if not node_type:
        node_type = "text"
    elif node_type != "group":
        if "Choose an asset" in text_value:
            text_value = None

        if node_type == "block":
            b_path = text_value
        elif node_type == "file":
            f_path = text_value
        elif node_type == "page":
            p_path = text_value
        asset_type = node_type
        text_value = None
        node_type = "asset"

    if children_list:
        children_list = turn_data_structure_into_nodes(children_list)

    to_return = {
        'assetType': asset_type,
        'blockPath': b_path,
        'filePath': f_path,
        'identifier': node_id,
        'pagePath': p_path,
        'structuredDataNodes': children_list,
        'text': text_value,
        'type': node_type
    }
    return to_return
