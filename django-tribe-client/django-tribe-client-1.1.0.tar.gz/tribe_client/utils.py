import requests
import json
from app_settings import *


def get_access_token(authorization_code):
    """
    Takes the temporary, short-lived authorization_code returned by tribe and
    sends it back (with some other ids and secrets) in exchange for an
    access_token.

    Arguments:
    authorization_code -- a string of characters returned by Tribe when it
    redirects the user from the page where they authorize the client to access
    their resources

    Returns:
    access_token -- another string of characters, with which users can remotely
    access their resources.

    """
    parameters = {"client_id": TRIBE_ID, "client_secret": TRIBE_SECRET, "grant_type": "authorization_code",  "code": authorization_code, "redirect_uri": TRIBE_REDIRECT_URI}
    tribe_connection = requests.post(ACCESS_TOKEN_URL, data=parameters)
    result = tribe_connection.json()
    if 'access_token' in result:
        access_token = result['access_token']
        return access_token
    else:
        return None

def retrieve_public_genesets(options={}):
    """
    Returns only public genesets
    """

    genesets_url = TRIBE_URL + '/api/v1/geneset/?format=json'

    for opt_key,opt in options.iteritems():
        genesets_url += '&'+opt_key+'='+opt

    try:
        tribe_connection = requests.get(genesets_url)
        result = tribe_connection.json()
        genesets = result['objects']
        return genesets

    except:
        return []


def retrieve_public_versions(options={}):
    """
    Returns only public versions
    """

    versions_url = TRIBE_URL + '/api/v1/version/?format=json'

    for opt_key,opt in options.iteritems():
        versions_url += '&'+opt_key+'='+opt

    try:
        tribe_connection = requests.get(versions_url)
        result = tribe_connection.json()
        versions = result['objects']
        return versions

    except:
        return []


def retrieve_user_object(access_token):
    """
    Makes a get request to tribe using the access_token to get the user's info
    (the user should only have permissions to see the user object that
    corresponds to them).

    Arguments:
    access_token -- The OAuth token with which the user has access to their
    resources. This is a string of characters.

    Returns:
    Either - 

    a) 'OAuth Token expired' if the access_token has expired,
    b) An empty list [] if the access_token is completely invalid, or
    c) The user object this user has access to (in the form of a dictionary)

    """

    parameters = {'oauth_consumer_key': access_token}

    try:
        tribe_connection = requests.get(TRIBE_URL + '/api/v1/user', params = parameters)
        result = tribe_connection.json()
        user = result['objects']  # This is in the form of a list
        meta = result['meta']

        if (meta.has_key('oauth_token_expired')):
            return ('OAuth Token expired')
        else:
            return user[0]  # Grab the first (and only) element in the list
    except:
        return []


def retrieve_user_genesets(access_token, options={}):
    """
    Returns genesets created by the user
    """

    try:
        get_user = retrieve_user_object(access_token)

        if (get_user == 'OAuth Token expired' or get_user == []):
            return ([])

        else:
            options['oauth_consumer_key'] = access_token
            options['creator'] = str(get_user['id'])
            options['show_tip'] = 'true'
            options['full_annotations'] = 'true'

            genesets_url = TRIBE_URL + '/api/v1/geneset/'

            tribe_connection = requests.get(genesets_url, params=options)
            result = tribe_connection.json()
            meta = result['meta']
            genesets = result['objects']
            return genesets

    except:
        return []


def retrieve_user_versions(access_token, geneset):
    """
    Returns all versions that belong to a specific geneset
    (if user has access to that geneset)
    """

    try:
        parameters = {'oauth_consumer_key': access_token}

        versions_url = TRIBE_URL + '/api/v1/version/?geneset__id=' + geneset + CROSSREF_DB
        tribe_connection = requests.get(versions_url, params=parameters)
        result = tribe_connection.json()
        meta = result['meta']
        versions = result['objects']
        return versions

    except:
        return []

def retrieve_all_user_versions(access_token):

    try:
        parameters = {'oauth_consumer_key': access_token}

        versions_url = TRIBE_URL + '/api/v1/version/?' + CROSSREF_DB + '&show_tip=true'
        tribe_connection = requests.get(versions_url, params=parameters)
        result = tribe_connection.json()
        meta = result['meta']
        versions = result['objects']
        return versions

    except:
        return []

def create_remote_geneset(access_token, geneset_info):

    if 'organism' in geneset_info:
        scientific_name = geneset_info['organism']
        organism_request = requests.get(TRIBE_URL + '/api/v1/organism?scientific_name=' + str(scientific_name))
        response = organism_request.json()
        organism = response['objects'][0]
        geneset_info['organism'] = organism['resource_uri']

    try:
        headers = {'AUTH': 'OAuth ' + access_token, 'Content-Type': 'application/json'}
        payload = json.dumps(geneset_info)
        genesets_url = TRIBE_URL + '/api/v1/geneset'
        r = requests.post(genesets_url, data=payload, headers=headers)
        response = r.json()
        return response

    except:
        return []

def create_remote_version(access_token, version_info):

    try:
        headers = {'AUTH': 'OAuth' + access_token, 'Content-Type': 'application/json'}
        payload = json.dumps(version_info)
        versions_url = TRIBE_URL + '/api/v1/version'
        r = requests.post(versions_url, data=payload, headers=headers)
        response = r.json()
        return response
    except:
        return []

def return_user_object(access_token):
    parameters = {'oauth_consumer_key': access_token}
    tribe_connection = requests.get(TRIBE_URL + '/api/v1/user', params = parameters)

    try:
        result = tribe_connection.json()
        return result
    except:
        result = '{"meta": {"previous": null, "total_count": 0, "offset": 0, "limit": 20, "next": null}, "objects": []}'
        result = json.loads(result)
        return result


def obtain_token_using_credentials(username, password, client_id, client_secret):
    oauth_url = TRIBE_URL + '/oauth2/token/'
    payload = {'grant_type': 'password', 'username': username, 'password': password, 'client_id': client_id, 'client_secret': client_secret}
    r = requests.post(oauth_url, data=payload)
    tribe_response = r.json()
    return tribe_response['access_token']
