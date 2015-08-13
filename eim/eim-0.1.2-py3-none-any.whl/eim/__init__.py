import pymongo

def connect():
    """
    Connects to the Emotion in Motion database and authenticates as the public, read-only `eim` user.

    :return: The `eim` database on the Emotion in Motion database server.
    :rtype: pymongo.Database
    """

    # Create client, connect to database, and authenticate
    client = pymongo.MongoClient('db0.musicsensorsemotion.com')
    db = client.eim
    db.authenticate('eim','eim')

    return db

def get_random_document(collection, filter=None):
    """
    Retrieves a random document from the specified collection that matches the filter dictionary.

    :param collection: The collection in the database from which to retrieve a random document.
    :type collection: pymongo.Collection
    :param filter: A filter to use as the search query.
    :type filter: dict
    :return: The randomly selected document.
    :rtype: dict
    """

    # If a filter wasn't passed, give it an empty dict
    # and a random number
    from random import random
    actual_filter = filter or {}
    actual_filter['random'] = {'$lte': random()}

    # Get document
    random_document = collection.find_one(filter=actual_filter, sort=[('random', pymongo.DESCENDING)])

    # Make sure we retrieved a document
    assert isinstance(random_document, dict), 'A MongoDB document was not returned by pymongo.collection.find_one(). There may not be a "random" field on documents in this collection.'
    return random_document

def get_random_documents(collection, count, filter=None):
    """
    Retrieves a list of random documents from the specified collection, each of which match the filter dictionary.

    :param collection: The collection in the database from which to retrieve the random documents.
    :type collection: pymongo.Collection
    :param count: The number of random documents to retrieve.
    :type count: int
    :param filter:  A filter to use as the search query.
    :type filter: dict
    :return: The list of randomly selected documents.
    :rtype: list
    """

    # Empty list for docs
    docs = []

    # Repeatedly call get_random_document to get docs

    for i in range(count):
        docs.append(get_random_document(collection, filter=filter))

    return docs

def all_keys(dictionary, sep='.', parent_key='', only_leaves=True):
    """
    Extracts all keys of a dictionary and returns them as a list.

    This method works only for dictionaries that would qualify as JSON. In other words, only those dictionaries that
    contain atomic types, lists, and other dictionaries will work with this method. Keys are joined together using the
    string specified in `sep`. Only 'leaf' keys will be extracted when `only_leaves` is `True` (default). The entries
    of lists will be represented as single numbers in the 'keypath'. For instance, in `{'foo': [1,2,3]}`, the extracted
    keys would be `foo.0`, `foo.1`, and `foo.2`.

    :param dictionary: The dictionary from which to extract keys.
    :type dictionary: dict
    :param sep: The string to use in concatenating keypaths.
    :type sep: str
    :param parent_key: The prefix keypath--used in recursive calls.
    :type parent_key: str
    :param only_leaves: If `True`, only 'leaf' keys will be extracted.
    :type only_leaves: bool
    :return: Returns the list of extracted keys.
    :rtype: list

    >>> a_dict = {'foo': 'bar'}
    >>> dict_keys = all_keys(a_dict)
    >>> set(dict_keys) == set(['foo'])
    True

    >>> a_dict = {'foo': [1,2,3]}
    >>> dict_keys = all_keys(a_dict)
    >>> set(dict_keys) == set(['foo.0', 'foo.1', 'foo.2'])
    True

    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> dict_keys = all_keys(a_dict)
    >>> set(dict_keys) == set(['foo.0.bar', 'foo.1', 'foo.2'])
    True

    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> dict_keys = all_keys(a_dict, only_leaves=False)
    >>> set(dict_keys) == set(['foo', 'foo.0', 'foo.1', 'foo.2', 'foo.0.bar'])
    True
    """

    import collections

    key_set = set()

    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key

        if isinstance(value, collections.MutableMapping):
            if not only_leaves:
                key_set.add(new_key)

            children = all_keys(value, sep=sep, parent_key=new_key, only_leaves=only_leaves)
            key_set = key_set.union(children)
        elif isinstance(value, list):
            if not only_leaves:
                key_set.add(new_key)

            for i in range(len(value)):
                list_index_key = new_key + sep + str(i)
                if not only_leaves:
                    key_set.add(list_index_key)

                # Recurse if the list entry is a dict
                if isinstance(value[i], dict):
                    children = all_keys(value[i], sep=sep, parent_key=list_index_key, only_leaves=only_leaves)
                    key_set = key_set.union(children)

                # Otherwise, just add a key with the index in dot notation
                else:
                    key_set.add(new_key + sep + str(i))
        else:
            key_set.add(new_key)

    return list(key_set)

def dict_value_for_keypath(dictionary, keypath, sep='.'):
    """
    Traverses the `sep`-delimited 'keypath' in `dictionary` and returns its value.

    This method works only for dictionaries that would qualify as JSON. In other words, only those dictionaries that
    contain atomic types, lists, and other dictionaries will work with this method. Keypaths are split by `sep`, and
    these individual keys are used to traverse the dictionary.

    :param dictionary: The dictionary to traverse.
    :type dictionary: dict
    :param keypath: The `sep`-delimited compound keypath.
    :type keypath: str
    :param sep: The delimiter used in building the keypath.
    :type sep: str
    :return: Returns the value for the keypath. This may be a `dict` or `list`.

    >>> a_dict = {'foo': 'bar'}
    >>> val = dict_value_for_keypath(a_dict, 'foo')
    >>> val == 'bar'
    True

    >>> a_dict = {'foo': [1,2,3]}
    >>> val = dict_value_for_keypath(a_dict, 'foo.1')
    >>> val == 2
    True

    >>> a_dict = {'foo': [{'bar':1},2,3]}
    >>> val = dict_value_for_keypath(a_dict, 'foo.0.bar')
    >>> val == 1
    True
    >>> val = dict_value_for_keypath(a_dict, 'foo.1')
    >>> val == 2
    True
    >>> val = dict_value_for_keypath(a_dict, 'foo.0')
    >>> val == {'bar': 1}
    True
    >>> val = dict_value_for_keypath(a_dict, 'foo.3')
    Traceback (most recent call last):
        ...
    IndexError: list index out of range

    >>> a_dict = {'foo': [{'bar':[{'baz': 'cheese'}]}]}
    >>> val = dict_value_for_keypath(a_dict, 'foo.0.bar.0.baz')
    >>> val == 'cheese'
    True
    """

    import collections

    if keypath == '':
        return dictionary

    key_list = keypath.split(sep=sep)

    value_for_key = None

    remaining_keypath = sep.join(key_list[1:])

    # pprint(dictionary)

    if isinstance(dictionary, collections.MutableMapping):
        value_for_key = dict_value_for_keypath(dictionary[key_list[0]], remaining_keypath, sep)
    elif isinstance(dictionary, list):
        value_for_key = dict_value_for_keypath(dictionary[int(key_list[0])], remaining_keypath, sep)

    return value_for_key
