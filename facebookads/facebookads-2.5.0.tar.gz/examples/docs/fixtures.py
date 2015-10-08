# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from facebookads import (
    exceptions,
    test_config,
    FacebookAdsApi,
    FacebookSession
)
from facebookads.objects import (
    AdAccount,
    Campaign,
    AdLabel,
    AdVideo,
    AdImage,
    AdSet,
    AdsPixel,
    AdCreative,
    Ad,
    CustomAudience
)
from facebookads.specs import LinkData, ObjectStorySpec

import time
import atexit

default_url = 'https://graph.facebook.com/' + FacebookAdsApi.API_VERSION
default_api = FacebookAdsApi.get_default_api()


def api_get(path, params=None, api=default_api, url=default_url):
    if params is None:
        params = {}
    response = api.call('GET', url + path)
    return response.json()


def api_delete(path, params=None, api=default_api, url=default_url):
    if params is None:
        params = {}
    response = api.call('DELETE', url + path, params=params)
    return response.json()


def api_post(path, params=None, api=default_api, url=default_url, **kwargs):
    if params is None:
        params = {}
    response = api.call('POST', url + path, params=params, **kwargs)
    return response.json()


def get_app(app_id=test_config.app_id):
    return api_get('/{}'.format(app_id))


def business_pixels(business_id):
    return api_get("/{}/adspixels".format(business_id))['data']


def can_see_business(business_id):
    for business in api_get('/me/businesses')['data']:
        if business_id == business['id']:
            return True
    return False


def can_see_account(account_id):
    for account in api_get('/me/adaccounts')['data']:
        if account_id in account['id']:
            return True
    return False


def unshare_pixel_from_agency(pixel_id, business_id, agency_id):
    params = {
        'business': business_id,
        'agency_id': agency_id
    }
    for pixel in business_pixels(agency_id):
        if pixel['id'] == pixel_id:
            api_delete('/' + pixel_id + '/shared_agencies', params=params)


def get_page_access_token():
    data = api_get('/me/accounts')['data']
    for page in data:
        if page['id'] == str(test_config.page_id):
            return page['access_token']
    raise 'Page access token for page id {} not found.'.\
        format(test_config.page_id)


def get_page_api():
    page_token = get_page_access_token()
    session = FacebookSession(test_config.app_id,
                              test_config.app_secret,
                              page_token)
    return FacebookAdsApi(session)


def create_product_set(product_catalog_id=None, params=None):
    if product_catalog_id is None:
        product_catalog_id = create_product_catalog()['id']

    if params is None:
        params = {}

    if 'name' not in params:
        params['name'] = unique_name('Test Product Set ')

    return api_post('/' + product_catalog_id + '/product_sets', params)


def create_product_catalog(params=None):
    if params is None:
        params = {}

    if 'name' not in params:
        params['name'] = unique_name('Test Catalog ')

    return api_post('/' + test_config.business_id + '/product_catalogs', params)


def get_promotable_post():
    api = get_page_api()
    path = "/{}/promotable_posts".format(test_config.page_id)
    posts = api_get(path, api=api)['data']

    if len(posts) == 0:
        raise "Could not find any promotable posts on your page"

    return posts[0]


def create_post(**params):
    if 'message' not in params:
        params['message'] = unique_name('Test Post ')
    api = get_page_api()
    path = "/{}/feed".format(test_config.page_id)

    return api_post(path, params=params, api=api)


def upload_video(video_path):
    api = get_page_api()
    path = "/{}/videos".format(test_config.page_id)
    url = 'https://graph-video.facebook.com/' + FacebookAdsApi.API_VERSION
    args = {'files': {'source': open(video_path)}}

    return api_post(path, api=api, url=url, args=args)


def remote_delete(obj):
    try:
        obj.remote_delete()
    except exceptions.FacebookRequestError:
        print("warning: could not delete {}".format(obj))


def delete_image(image):
    image_hash = image[AdImage.Field.hash]
    image_id = image[AdImage.Field.id]
    image = AdImage(image_id, test_config.account_id)
    image.remote_delete(params={AdImage.Field.hash: image_hash()})


def create_campaign(params=None):
    if params is None:
        params = {}

    campaign = Campaign(parent_id=test_config.account_id)
    campaign[Campaign.Field.name] = unique_name('Test Campaign')
    campaign[Campaign.Field.buying_type] = Campaign.BuyingType.auction
    campaign[Campaign.Field.objective] = Campaign.Objective.link_clicks
    campaign[Campaign.Field.status] = Campaign.Status.paused

    campaign.update(params)
    campaign.remote_create()

    atexit.register(remote_delete, campaign)

    return campaign


def create_image():
    image = AdImage(parent_id=test_config.account_id)
    image[AdImage.Field.filename] = test_config.image_path
    image.remote_create()

    # FIXLATER: properly delete images with dependencies

    return image


def create_video():
    video = AdVideo(parent_id=test_config.account_id)
    video[AdVideo.Field.filepath] = test_config.video_path
    video.remote_create()
    video.waitUntilEncodingReady()

    atexit.register(remote_delete, video)

    return video


def unique_name(base_name):
    return base_name + ' ' + str(time.clock())


def create_creative(image=None):
    if image is None:
        image = create_image()

    image_hash = image.get_hash()

    link_data = LinkData()
    link_data[LinkData.Field.message] = 'try it out'
    link_data[LinkData.Field.link] = 'http://example.com'
    link_data[LinkData.Field.caption] = 'www.example.com'
    link_data[LinkData.Field.image_hash] = image_hash

    object_story_spec = ObjectStorySpec()
    object_story_spec[ObjectStorySpec.Field.page_id] = test_config.page_id
    object_story_spec[ObjectStorySpec.Field.link_data] = link_data

    creative = AdCreative(parent_id=test_config.account_id)
    creative[AdCreative.Field.name] = unique_name('Test Creative')
    creative[AdCreative.Field.object_story_spec] = object_story_spec
    creative.remote_create()

    atexit.register(remote_delete, creative)

    return creative


def create_custom_audience():
    audience = CustomAudience(parent_id=test_config.account_id)
    audience[CustomAudience.Field.subtype] = CustomAudience.Subtype.custom
    audience[CustomAudience.Field.name] = unique_name('Test Audience')
    audience[CustomAudience.Field.description] = 'Created for docsmith example'
    audience.remote_create()

    atexit.register(remote_delete, audience)

    return audience


def create_ads_pixel():
    account = AdAccount(test_config.account_id)
    pixel = account.get_ads_pixels([AdsPixel.Field.code])

    if pixel is None:
        pixel = AdsPixel(parent_id=test_config.account_id)
        pixel[AdsPixel.Field.name] = unique_name('Test Pixel')
        pixel.remote_create()

    return pixel


def create_adset(campaign=None):
    if campaign is None:
        campaign = create_campaign()

    adset = AdSet(parent_id=test_config.account_id)
    adset[AdSet.Field.name] = unique_name('Test Adset')
    adset[AdSet.Field.campaign_id] = campaign.get_id()
    adset[AdSet.Field.targeting] = {
        'geo_locations': {
            'countries': ['US']
        }
    }
    adset[AdSet.Field.optimization_goal] = AdSet.OptimizationGoal.impressions
    adset[AdSet.Field.billing_event] = AdSet.BillingEvent.impressions
    adset[AdSet.Field.bid_amount] = 100
    adset[AdSet.Field.daily_budget] = 1000
    adset.remote_create()

    atexit.register(remote_delete, adset)

    return adset


def create_ad(ad_set=None, creative=None):
    if ad_set is None:
        ad_set = create_adset()

    if creative is None:
        creative = create_creative()

    ad = Ad(parent_id=test_config.account_id)
    ad[Ad.Field.name] = unique_name('My Ad')
    ad[Ad.Field.adset_id] = ad_set.get_id_assured()
    ad[Ad.Field.status] = Ad.Status.paused
    ad[Ad.Field.creative] = {
        'creative_id': creative.get_id_assured(),
    }
    ad.remote_create()

    atexit.register(remote_delete, ad)

    return ad


def create_adlabel(params={}):
    adlabel = AdLabel(parent_id=test_config.account_id)
    adlabel[AdLabel.Field.name] = unique_name('Label Name')
    adlabel.update(params)
    adlabel.remote_create()

    atexit.register(remote_delete, adlabel)

    return adlabel
