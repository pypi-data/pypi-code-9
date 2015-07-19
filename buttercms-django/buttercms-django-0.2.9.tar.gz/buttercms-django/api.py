from django.conf import settings
from django.http import Http404

import requests


DEFAULT_TOKEN = 'f97d131d955f48af0769a4c827bb47728cbd5d05'
API_URL = 'https://buttercms.com/api/'


class ButterCms(object):
    def __init__(self):
        try:
            self.api_key = settings.BUTTER_CMS_TOKEN
        except AttributeError:
            self.api_key = DEFAULT_TOKEN

    def get_auth_header(self):
        return {'Authorization': 'Token %s' % self.api_key}

    def get_posts(self, page):

        if page:
            page_param = '?page=%s' % page
        else:
            page_param =''

        try:
            response = requests.get('%sposts/%s' % (API_URL, page_param), headers=self.get_auth_header())
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # If we get a 401 then the token is likely bad.
            if response.status_code == 401:
                raise Http404("This token has not been registered. Please get a new one and register - https://buttercms.com/api_token/")
            if response.status_code == 404:
                raise Http404("Blog does not exist.")
        except:
            raise Http404("An error occured retrieving blog. Please try again later.")

        return response.json()

    def get_post(self, slug):
        try:
            response = requests.get('%sposts/%s' % (API_URL, slug), headers=self.get_auth_header())
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # If we get a 401 then the token is likely bad.
            if response.status_code == 401:
                raise Http404("This token has not been registered. Please get a new one and register - https://buttercms.com/api_token/")
            if response.status_code == 404:
                raise Http404("Blog post does not exist.")
        except:
            raise Http404("An error occured retrieving blog post. Please try again later.")

        return response.json()

    def get_author(self, author_slug):
        try:
            response = requests.get('%sauthors/%s' % (API_URL, author_slug), headers=self.get_auth_header())
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # If we get a 401 then the token is likely bad.
            if response.status_code == 401:
                raise Http404("This token has not been registered. Please get a new one and register - https://buttercms.com/api_token/")
            if response.status_code == 404:
                raise Http404("Author does not exist.")
        except:
            raise Http404("An error occured retrieving author page. Please try again later.")

        return response.json()


    def get_category(self, category_slug):
        try:
            response = requests.get('%scategories/%s' % (API_URL, category_slug), headers=self.get_auth_header())
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # If we get a 401 then the token is likely bad.
            if response.status_code == 401:
                raise Http404("This token has not been registered. Please get a new one and register - https://buttercms.com/api_token/")
            if response.status_code == 404:
                raise Http404("Category does not exist.")
        except:
            raise Http404("An error occured retrieving author page. Please try again later.")

        return response.json()


    

