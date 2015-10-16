#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_whiplash
----------------------------------

Tests for `whiplash` module.
"""

import pytest
import time
import logging

logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

from whiplash import Whiplash


@pytest.fixture
def client():
    return Whiplash('Hc2BHTn3bcrwyPooyYTP', True)


def test_item(client):
    sku = 'FULFIL:SKU-%d' % time.time()
    group_id = 'Fulfil_IO Test Products'

    # Create product
    product = client.item.create(
        title='Imaginary Test Product',
        sku=sku,
        group_id=group_id,
    )

    # Assert that the response has same SKU
    assert product.sku == sku

    # Search and find the SKU by product
    product, = client.item.get_by(sku=sku)
    assert product.sku == sku

    # Search and find all SKUs fulfil.IO created
    products = client.item.get_by(group_id=group_id)
    assert len(products) > 0
