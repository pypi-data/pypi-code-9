from strawpoll import StrawpollAPIReader
from random import randrange

import requests

# Setup test fixtures for poll id `id`
id = randrange(1, 1000)
BASE_URL = 'https://strawpoll.me'
API_PATH = 'api/v2/polls'
json = requests.get('/'.join([BASE_URL, API_PATH, str(id)]))
sp = dict(json=json.text, api=StrawpollAPIReader.from_apiv2(id), url=StrawpollAPIReader.from_url('/'.join([BASE_URL, str(id)])))

# I feel these are redundant since we only need to test URL vs JSON
# to actually verify if everything is working due to how this is layered
def test_json_and_api_return_same_data():
    assert(StrawpollAPIReader.from_json(sp['json']) == sp['api'])

# @with_setup(setup, teardown)
def test_api_and_url_return_same_data():
    assert(sp['api'] == sp['url'])

# @with_setup(setup, teardown)
def test_json_and_url_return_same_data():
    assert(StrawpollAPIReader.from_json(sp['json']) == sp['url'])
