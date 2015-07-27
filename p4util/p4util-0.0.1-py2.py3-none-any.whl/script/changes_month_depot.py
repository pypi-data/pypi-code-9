#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Copyright (c) 2013 Sven Erik Knop, Perforce Software Ltd
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1.  Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#
# 2.  Redistributions in binary form must reproduce the above copyright
#         notice, this list of conditions and the following disclaimer in the
#         documentation and/or other materials provided with the
#         distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PERFORCE
# SOFTWARE, INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# User contributed content on the Perforce Public Depot is not supported by Perforce,
# although it may be supported by its author. This applies to all contributions
# even those submitted by Perforce employees.
#
# Maintainer: Sven Erik Knop, sknop@perforce.com

# this module requires the following additional Python modules
#
# P4Python (www.perforce.com)

from __future__ import print_function

import P4
import re, sys
from datetime import date 
import argparse
from pprint import pprint

MONTHS=60 # 5 years, overriden by option

class GrowthMonthDepot:
    def __init__(self, months, output):
        self.months = months
        self.p4 = P4.P4()
        self.p4.prog = "Change analyzer"
        self.p4.connect()

        self.depots = [ x['name'].lower() for x in self.p4.run_depots() if not x['type'] in ['spec', 'archive', 'unload'] ]
        self.depots.append('...') # catch all for changes spanning more than one depot
        self.changes = {}
        self.sizes = {}
                    
        self.get_changes_and_sizes()

        self.out = sys.stdout
        if output:
            self.out = open(output, "w")

    def month_range(self, months):
       now = date.today()
       end_year = now.year
       end_month = now.month + 1
       for m in range(months):
            start_year = end_year
            start_month = end_month - 1
            if start_month == 0:
                start_month = 12
                start_year -= 1

            date_range = "@{sy}/{sm}/1,@{ey}/{em}/1".format(sy = start_year, sm = start_month, ey = end_year, em = end_month)
            year_month = "{year}/{month:02}".format(year=start_year, month=start_month)
            
            yield (date_range, year_month)

            end_year = start_year
            end_month = start_month

    def sort_changes_by_depot(self, changes):
        # initalize
        result = {}
        for depot in self.depots:
            result[depot] = 0

        pattern = re.compile("//([^/]+).*")

        for change in changes:
            m = pattern.match(change['path'])
            if m:
                depot = pattern.match(change['path']).group(1)
                depot = depot.lower()
                if not depot in result:
                    depot = '...'
            else:
                continue

            result[depot] = result[depot] + 1

        return result
    
    def get_sizes(self, date_range, changes_per_depot):
        result = {}
        for depot in changes_per_depot:
            if depot not in ['...'] and changes_per_depot[depot] > 0:
                path = "//{depot}/...{range}".format(depot=depot, range=date_range)
                result[depot] = int(self.p4.run_sizes("-sa", path)[0]['fileSize'])
            else:
                result[depot] = 0
        return result

    def get_changes_and_sizes(self):

        for (date_range, year_month) in self.month_range(self.months):
            ch = self.p4.run_changes("-ssubmitted", date_range)
            print("{m} : {total}".format(m=year_month, total=len(ch)))

            self.changes[year_month] = self.sort_changes_by_depot(ch)

            self.sizes[year_month] = self.get_sizes(date_range, self.changes[year_month])
    
    def print_headers(self):
        print("month", end=',', file=self.out)
        for depot in sorted(self.depots):
            print(depot,end=',', file=self.out)
        print(file=self.out)
                                                              
    def print_changes(self):
        for ym in sorted(self.changes, reverse=True):
            print(ym,end=',', file=self.out)
            changes_for_depots = self.changes[ym]
            d = sorted(changes_for_depots.keys())
            for ch in d:
                print(changes_for_depots[ch],end=',', file=self.out)
            print(file=self.out)


    def print_sizes(self):
        for ym in sorted(self.sizes, reverse=True):
            print(ym,end=',', file=self.out)
            sizes_for_depots = self.sizes[ym]
            d = sorted(sizes_for_depots.keys())
            for ch in d:
                print(sizes_for_depots[ch],end=',', file=self.out)
            print(file=self.out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change analyzer")
    parser.add_argument("-m","--months", default=MONTHS, type=int)
    parser.add_argument("-o","--output", default=None)
    args = parser.parse_args()
    months = args.months
    output = args.output

    analyzer = GrowthMonthDepot(months, output)
  
    analyzer.print_headers() 
    analyzer.print_changes()
    analyzer.print_headers() 
    analyzer.print_sizes()
     
