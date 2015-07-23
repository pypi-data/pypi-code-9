#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Farfetch API
# Copyright (C) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Farfetch API.
#
# Hive Farfetch API is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Farfetch API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Farfetch API. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Rui Castro <rui.castro@gmail.com>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class UserApi(object):

    def create_user(self, user):
        url = self.base_url + "users"
        contents = self.post(url, data_j = user)
        return contents

    def show_user(self, id):
        url = self.base_url + "users/%s" % id
        contents = self.get(url)
        return contents

    def show_my_user(self):
        # @todo: change this method naming: me_user
        url = self.base_url + "users/Me"
        contents = self.get(url)
        return contents

    def update_user(self, id, user):
        url = self.base_url + "users/%s" % id
        contents = self.put(url, data_j = user)
        return contents

    def request_password_reset(self, email):
        #@todo: change method name: recovery_password_user
        url = self.base_url + "users/password-recovery"
        contents = self.post(url, data_j = dict(email = email))
        return contents

    def reset_password(self, email, token, password):
        #@todo: change method name: reset_password_user
        url = self.base_url + "users/password-change"
        contents = self.post(
            url,
            data_j = dict(
                email = email,
                token = token,
                password = password
            )
        )
        return contents

    def change_password(self, id, username, old_password, new_password):
        #@todo: change method naming change_password_user
        url = self.base_url + "users/%s/password-change" % id
        contents = self.post(
            url,
            data_j = dict(
                oldPassword = old_password,
                newPassword = new_password,
                username = username
            )
        )
        return contents

    def list_addresses(self, user_id, type = None, page = None, page_size = None):
        #@todo: change method naming list_addresses_user
        url = self.base_url + "users/%s/addresses" % user_id
        params = dict(
            type = type,
            page = page,
            pageSize = page_size
        )
        contents = self.get(url, params=params)
        return contents

    def list_billing_addresses(self, user_id, page = None, page_size = None):
        #@todo: rename billing_addresses_user
        return self.list_addresses(
            user_id,
            type = "Billing",
            page = page,
            page_size = page_size
        )

    def list_shipping_addresses(self, user_id, page = None, page_size = None):
        #@todo: rename shipping_addresses_user
        return self.list_addresses(user_id, "Shipping", page, page_size)

    def show_address(self, user_id, address_id):
        #@todo: rename address_user
        url = self.base_url + "users/%s/addresses/%s" % (user_id, address_id)
        contents = self.get(url)
        return contents

    def show_shipping_address(self, user_id):
        #@todo: shipping_address_user
        url = self.base_url + "users/%s/addresses/shipping/current" % user_id
        contents = self.get(url)
        return contents

    def show_billing_address(self, user_id):
        #@todo: billing_address_user
        url = self.base_url + "users/%s/addresses/billing/current" % user_id
        contents = self.get(url)
        return contents

    def create_address(self, user_id, address):
        #@todo: create_address_user
        url = self.base_url + "users/%s/addresses" % user_id
        contents = self.post(url, data_j = address)
        return contents

    def update_address(self, user_id, address_id, address):
        #@todo: update_address_user
        url = self.base_url + "users/%s/addresses/%s" % (user_id, address_id)
        contents = self.put(url, data_j = address)
        return contents

    def delete_address(self, user_id, address_id):
        #@todo: delete_address_user
        url = self.base_url + "users/%s/addresses/%s" % (user_id, address_id)
        contents = self.delete(url)
        return contents

    def list_orders(self, user_id, page = None, page_size = None):
        #@todo: orders_user
        url = self.base_url + "users/%s/orders" % user_id
        params = dict(
            page = page,
            pageSize = page_size
        )
        contents = self.get(url, params = params)
        return contents

    def list_payments(self, user_id, page = None, page_size = None):
        #@todo: payments_user
        url = self.base_url + "users/%s/tokens" % user_id
        params = dict(
            page = page,
            pageSize = page_size
        )
        contents = self.get(url, params = params)
        return contents

    def create_guest_user(self, country_code, ip):
        url = self.base_url + "guestUsers"
        guest_user = dict(countryCode = country_code, ip = ip)
        return self.post(url, data_j = guest_user)

    def show_guest_user(self, id):
        url = self.base_url + "guestUsers/%s" % id
        return self.get(url)
