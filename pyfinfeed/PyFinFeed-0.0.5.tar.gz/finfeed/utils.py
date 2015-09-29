#! /usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

class UtilsMixin(object):
    """Handles some basic data munging."""

    GAAP_ENDPOINT = "/stock_gaap/"

    def basic_dataframe(self, tags, fiscal_years, stocks):
        payload = {'stocks': stocks, 'tags': tags, 'fiscal_years': fiscal_years, 'group_by': 'tags'}
        data = self.get(self.GAAP_ENDPOINT, params=payload)
        json = data.json()
        dataframe = {}
        for tag in json['gaap']:

            all_data = {}
            for tickers in json['gaap'][tag]:
                values = json['gaap'][tag][tickers]

                points = {}
                for value in values:
                    values = json['gaap'][tag][tickers]
                    points[value['fiscal_year']] = value['value']

                all_data[tickers] = points

            dataframe[tag] = all_data

        return dataframe
