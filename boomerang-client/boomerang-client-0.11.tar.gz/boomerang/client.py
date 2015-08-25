# -*- coding: utf-8 -*-
import urlparse
import requests

__author__ = 'ola'


class BoomerangClient:

    BASE_URL = 'http://api.boomerang.io/v1'

    def __init__(self, project_id, api_key):
        self.url = "%s/api_key/%s/projects/%s/boomerangs/" % (self.BASE_URL, api_key, project_id)

    def boomerang_url(self, bid):
        return urlparse.urljoin(self.url, bid)


    def get_all_boomerangs(self):
        res = requests.get(self.url)
        return res


    def get_one_boomerang(self, boomerang_id):
        res = requests.get(self.boomerang_url(boomerang_id))
        return res


    def create_boomerang(self, params):
        res = requests.post(self.url, params)
        return res


    def update_boomerang(self, boomerang_id):
        res = requests.put(self.boomerang_url(boomerang_id))
        return res


    def delete_boomerang(self, boomerang_id):
        res = requests.delete(self.boomerang_url(boomerang_id))
        return res
