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

from onyx.core import (Curve, HlocvCurve, Knot, LYY2Date,
                       DelObj, UpdateObj, ObjNotFound,
                       GetVal, SetVal, TsDbGetCurve, TsDbQuery, TsNotFound,
                       GraphNodeVt, StringField, DictField, ReferenceField)

from agora.corelibs.date_functions import DateOffset
from agora.corelibs.ufo_functions import InheritAsProperty, RetainedFactory
from agora.system.ufo_asset import Asset

__all__ = ["CommodCnt"]

# --- replace all base class stored attributes with pointers to CommodAsset,
#     with the exception of RiskProxy
REPLACE = Asset._json_fields.difference({"RiskProxy"})
# --- add a few CommodAsset-specific stored attributes
REPLACE = REPLACE.union({"Market", "CntType", "ContractSize", "SettDateRule",
                         "OptExpDateRule", "Country", "Region", "Sector",
                         "Subsector"})


###############################################################################
@InheritAsProperty(REPLACE, "CommodAsset")
class CommodCnt(Asset):
    """
    This class used to access commod contract information and the relative
    timeseries.
    """
    # --- this is the parent object that babysits all contracts on the same
    #     commodity
    CommodAsset = ReferenceField(obj_type="CommodAsset")
    Tickers = DictField()

    # --- DeliveryMonth is the LYY code for the contract
    DeliveryMonth = StringField()

    Marks = StringField()
    TimeSeries = StringField()

    # -------------------------------------------------------------------------
    def __post_init__(self):
        mkt = GetVal(self.CommodAsset, "Market")
        sym = GetVal(self.CommodAsset, "Symbol")
        args = mkt, sym, self.DeliveryMonth

        self.Name = self.get_name(*args)
        self.Marks = "CNT-MKS {0:s} {1:s} {2:3s}".format(*args)
        self.TimeSeries = "CNT-TS {0:s} {1:s} {2:3s}".format(*args)

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def Ticker(self, graph, platform="Bloomberg"):
        """
        If ticker for a given platform is missing, it's understood that we
        should default to the one for Bloomberg.
        """
        try:
            return graph(self, "Tickers")[platform]
        except KeyError:
            return graph(self, "Tickers")["Bloomberg"]

    # -------------------------------------------------------------------------
    @GraphNodeVt("Property")
    def UniqueId(self, graph):
        mkt = graph(self, "Market")
        sym = graph(self, "Symbol")
        mth = graph(self, "DeliveryMonth")
        return "{0:s} {1:s} {2:3s}".format(mkt, sym, mth)

    # -------------------------------------------------------------------------
    @GraphNodeVt("Property")
    def FutSettDate(self, graph):
        rule = graph(self, "SettDateRule")
        cal = graph(self, "HolidayCalendar")
        mth = graph(self, "DeliveryMonth")
        return DateOffset(LYY2Date(mth), rule, cal)

    # -------------------------------------------------------------------------
    @GraphNodeVt("Property")
    def VolEndDate(self, graph):
        return graph(self, "FutSettDate")

    # -------------------------------------------------------------------------
    @GraphNodeVt("Property")
    def OptExpDate(self, graph):
        rule = graph(self, "OptExpDateRule")
        cal = graph(self, "HolidayCalendar")
        return DateOffset(graph(self, "FutSettDate"), rule, cal)

    # -------------------------------------------------------------------------
    @RetainedFactory()
    def Spot(self, graph):
        """
        Return the official close value as of MktDataDate (or the most recent
        close if ForceStrict is False) in the Denominated currency.
        """
        prc = graph(graph(self, "Marks"), "Price")
        return prc*graph(self, "Multiplier")

    # -------------------------------------------------------------------------
    @GraphNodeVt("Property")
    def Last(self, graph):
        """
        Return the knot with the most recent close value irrespective of
        MktDataDate in the Denominated currency.
        """
        marks = graph(self, "Marks")
        date = graph(marks, "LastBefore")
        value = graph(marks, "PrcByDate", date, strict=True)
        return Knot(date, value*graph(self, "Multiplier"))

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def GetCurve(self, graph, start=None, end=None, field=None):
        name = graph(self, "TimeSeries")
        if graph(self, "CntType") == "HLOCV":
            try:
                return TsDbGetCurve(name, start, end, "HLOCV", field)
            except TsNotFound:
                return HlocvCurve()
        else:
            try:
                return TsDbGetCurve(name, start, end, "CRV", field)
            except TsNotFound:
                return Curve()

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def GetMarks(self, graph, start=None, end=None):
        return graph(graph(self, "Marks"), "PrcFixCurve", start, end)

    # -------------------------------------------------------------------------
    def delete(self):
        # --- delete time-series from TsDb
        if self.CntType == "HLOCV":
            query = "DELETE FROM HlocvCurves WHERE Name=%s"
        else:
            query = "DELETE FROM Curves WHERE Name=%s"

        # --- delete timeseries
        TsDbQuery(query, parms=(self.TimeSeries,))

        # --- delete price fixes
        try:
            DelObj(self.Marks)
        except ObjNotFound:
            pass

        # --- remove from set of contracts for the CommodAsset object
        cnts = GetVal(self.CommodAsset, "Contracts")
        cnts.discard(self.DeliveryMonth)

        SetVal(self.CommodAsset, "Contracts", cnts)
        UpdateObj(self.CommodAsset)

    # -------------------------------------------------------------------------
    @classmethod
    def get_name(cls, market, symbol, del_mth):
        """
        Generate contract's name from Market, Symbol, and DeliveryMonth
        """
        return "CNT {0:s} {1:s} {2:3s}".format(market, symbol, del_mth)


# -----------------------------------------------------------------------------
def prepare_for_test():
    from onyx.core import Date, GetObj
    from agora.system.ufo_price_fix import PriceFix
    from agora.corelibs.unittest_utils import AddIfMissing

    import agora.system.ufo_commod_asset as ufo_commod_asset
    import agora.system.ufo_price_fix as ufo_price_fix

    ufo_commod_asset.prepare_for_test()
    ufo_price_fix.prepare_for_test()

    commod = GetObj("COMMOD CO2 EUA")
    cnt = commod.add_contract("Z15",  {"Bloomberg": "MOZ5"})

    prc_fix = AddIfMissing(PriceFix(Name=GetVal(cnt, "Marks")))
    prc_fix.add_dated("Price", Date.today(), 7.0)

    return [cnt]
