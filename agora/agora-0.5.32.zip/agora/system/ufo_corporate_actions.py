###############################################################################
#
#   Agora Portfolio & Risk Management System
#
#   Copyright 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from onyx.core import (Date, RDate, Curve, GCurve, HlocvCurve,
                       Interpolate, ApplyAdjustments, ListField,
                       ReferenceField, GraphNodeVt, ObjDbQuery)

from onyx.database.ufo_base import custom_decoder

from agora.system.ufo_archivable import Archivable
from agora.corelibs.ufo_functions import MktIndirectionFactory

import numpy as np
import collections
import json

__all__ = ["CorporateActions"]

# --- these are dividends paid as cash
CASH_ACTIONS = {"Regular Cash", "Special Cash", "Final",
                "Interim", "1st Interim", "2nd Interim",
                "3rd Interim", "4th Interim", "Return of Capital",
                "Return Prem.", "Interest on Capital", "Pro Rata",
                "Partnership Dist"}

# --- these are corporate action for which we mark the multiplicative
#     adjustment factor directly
MUL_ACTIONS = {"Open Offer", "Rights Issue",
               "Entitlement", "Spinoff", "Warrant", "In-specie"}

# --- these are corporate action for which we mark the divisive
#     adjustment factor directly
DIV_ACTIONS = {"Stock Split", "Bonus",
               "Stock Dividend", "Quote Lot Change"}

# --- these are corporate ations that don't affect historical prices
SKIP_ACTIONS = {"Cancelled", "Omitted", "Discontinued"}

GET_HISTORY_QUERY = """
SELECT Data->'_p_vt_data'->'{0:s}' as {0:s} FROM Archive WHERE Name=%s;"""


###############################################################################
class CorporateActions(Archivable):
    """
    Class used to represent corporate actions, archived by their Declared Date.
    """
    Asset = ReferenceField(obj_type="EquityAsset")
    DvdDenominated = ReferenceField(obj_type="Currency")

    # -------------------------------------------------------------------------
    @MktIndirectionFactory(ListField)
    def Info(self, graph):
        pass

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def NextExDateActions(self, graph, start):
        # FIXME: this is extremely inefficient, we should use a specialized
        #        query
        pd = graph("Database", "PositionsDate")
        crv = graph(self, "InfoCurve").crop(start=max(start, pd))
        if len(crv):
            return crv.front.value
        else:
            return [{"Ex-Date": Date.high_date(), "Dividend Type": None}]

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def FxAdjustment(self, graph, mdd):
        ccy = graph(graph(self, "Asset"), "Denominated")
        dvd_ccy = graph(self, "DvdDenominated")

        if ccy == dvd_ccy:
            return 1.0
        else:
            mul = graph(graph(self, "Asset"), "Multiplier")

            # --- dvd_ccy -> ccy
            to_usd = graph("{0:3s}/USD".format(dvd_ccy), "SpotByDate", mdd)
            to_ccy = 1.0 / graph("{0:3s}/USD".format(ccy), "SpotByDate", mdd)

            return to_usd * to_ccy / mul

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def InfoCurve(self, graph, by_date="Ex-Date"):
        query = GET_HISTORY_QUERY.format("Info")
        parms = (self.Name, )

        info_by_date = collections.defaultdict(list)

        for rec in ObjDbQuery(query, parms, attr="fetchall"):
            info = json.loads(rec.info, cls=custom_decoder)
            for item in info:
                info_by_date[item[by_date]].append(item)

        return GCurve(info_by_date.keys(), info_by_date.values())

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def DvdCurve(self, graph, start=None, end=None):
        """
        N.B.: we only include cash dividends here.
        """
        info_crv = graph(self, "InfoCurve").crop(start, end)

        dvd_crv = Curve()
        for _, value in info_crv:
            for action in value:
                if action["Dividend Type"] in CASH_ACTIONS:
                    date = action["Ex-Date"]
                    if date in dvd_crv:
                        dvd_crv[date] += action["Dividend Amount"]
                    else:
                        dvd_crv[date] = action["Dividend Amount"]

        return dvd_crv

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def AdjustCurve(self, graph, crv):
        start = crv.front.date
        end = crv.back.date

        if isinstance(crv, HlocvCurve):
            closes = crv.curve(field="close")
        else:
            closes = crv

        offset = RDate("-1b")
        adj_crv = Curve()

        for date, value in graph(self, "InfoCurve", by_date="Ex-Date"):

            if date == start:
                # --- remove this knot from the curve and skip this corporate
                #     action
                start += RDate("+1b")
                continue
            elif date < start or date > end:
                continue

            prev_biz_date = date + offset
            prev_close = Interpolate(closes, prev_biz_date)

            actions = [(info["Dividend Type"],
                        info["Dividend Amount"]) for info in value]

            cash, mul, div = [], [], []
            for dvd_type, amount in actions:
                if dvd_type in CASH_ACTIONS:
                    fx_adj = graph(self, "FxAdjustment", date)
                    cash.append(amount*fx_adj)
                elif dvd_type in MUL_ACTIONS:
                    mul.append(amount)
                elif dvd_type in DIV_ACTIONS:
                    div.append(amount)
                elif dvd_type in SKIP_ACTIONS:
                    continue
                else:
                    raise RuntimeError("Unknown Dividend Type {0:s} "
                                       "for {1:s}".format(dvd_type, self.Name))

            adj = 1.0 - sum(cash) / prev_close
            adj *= np.prod(mul)
            adj *= np.prod([1.0 / x for x in div])

            adj_crv[date] = adj

        adj_crv = Curve(adj_crv.dates,
                        np.cumprod(adj_crv.values[::-1])[::-1])

        return ApplyAdjustments(crv, adj_crv).crop(start=start, end=end)


# -----------------------------------------------------------------------------
def prepare_for_test():
    import agora.system.ufo_database as ufo_database
    ufo_database.prepare_for_test()
