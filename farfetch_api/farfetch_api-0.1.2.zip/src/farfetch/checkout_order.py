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

class CheckoutOrderApi(object):

    def show_checkout_order(self, id):
        url = self.base_url + "checkoutOrders/%s" % id
        contents = self.get(url)
        return contents

    def update_checkout_order(self, id, checkout_order):
        url = self.base_url + "checkoutOrders/%s" % id
        contents = self.put(url, data_j = checkout_order)
        return contents

    def update_checkout_order_addresses(
        self,
        id,
        shipping_address_id = None,
        shipping_address = None,
        billing_address_id = None,
        billing_address = None
    ):
        url = self.base_url + "checkoutOrders/%s" % id
        checkout_order = dict(
            shippingAddressId = shipping_address_id,
            shippingAddress = shipping_address,
            billingAddressId = billing_address_id,
            billingAddress = billing_address
        )
        contents = self.patch(url, data_j = checkout_order)
        return contents

    def list_shipping_options(self, id):
        url = self.base_url + "checkoutOrders/%s/shippingOptions" % id
        contents = self.get(url)
        return contents

    def update_shipping_options(self, id, shipping_options):
        url = self.base_url + "checkoutOrders/%s/shippingOptions" % id
        contents = self.put(url, data_j=shipping_options)
        return contents
