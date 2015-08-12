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
