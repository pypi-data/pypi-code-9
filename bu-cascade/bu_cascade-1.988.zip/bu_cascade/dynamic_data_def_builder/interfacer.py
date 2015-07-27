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
