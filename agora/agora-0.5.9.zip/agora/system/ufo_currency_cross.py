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

from onyx.core import (Curve, Knot, UfoBase, ReferenceField, StringField,
                       TsDbGetRowBy, TsDbGetCurve, TsDbUpsertCurve,
                       TsNotFound, GraphNodeVt)

from agora.corelibs.ufo_functions import RetainedFactory

__all__ = ["CurrencyCross"]


###############################################################################
class CurrencyCross(UfoBase):
    """
    Class used to represent a cross between two currencies (i.e. FX rates).
    """
    # --- conversion is Currency1 -> Currency2
    Currency1 = ReferenceField(obj_type="Currency")
    Currency2 = ReferenceField(obj_type="Currency")
    FxTimeSeries = StringField()

    # -------------------------------------------------------------------------
    def __post_init__(self):
        self.Name = "{0:3s}/{1:3s}".format(self.Currency1, self.Currency2)
        self.FxTimeSeries = "FX-TS {0:s}".format(self.Name)

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def Ticker(self, graph, platform="Bloomberg"):
        if platform == "Bloomberg":
            return "{0:3s}{1:3s} CURNCY".format(*self.Name.split("/"))
        else:
            raise NotImplementedError("Unrecognized "
                                      "platform {0:s}".format(platform))

    # -------------------------------------------------------------------------
    @RetainedFactory()
    def Spot(self, graph):
        """
        Return the official close value as of MktDataDate (or the most recent
        close if ForceStrict is False).
        """
        day = graph("Database", "MktDataDate")
        name = graph(self, "FxTimeSeries")
        row = TsDbGetRowBy("Curves", name,
                           day, graph("Database", "ForceStrict"))
        return row[2]

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def SpotByDate(self, graph, day):
        """
        Return the official close value as of the specified date (or the most
        recent close if ForceStrict is False).
        """
        name = graph(self, "FxTimeSeries")
        row = TsDbGetRowBy("Curves", name,
                           day, graph("Database", "ForceStrict"))
        return row[2]

    # -------------------------------------------------------------------------
    @GraphNodeVt("Property")
    def Last(self, graph):
        """
        Return the knot with the most recent close value irrespective of
        MktDataDate.
        """
        row = TsDbGetRowBy("Curves", graph(self, "FxTimeSeries"))
        return Knot(row.date, row.value)

    # -------------------------------------------------------------------------
    @GraphNodeVt()
    def GetCurve(self, graph, start=None, end=None):
        try:
            return TsDbGetCurve(graph(self, "FxTimeSeries"), start, end)
        except TsNotFound:
            return Curve()

    # -------------------------------------------------------------------------
    def UpdateTimeSeries(self, data):
        if isinstance(data, (tuple, list)):
            data = Curve([data[0]], [data[1]])

        TsDbUpsertCurve(self.FxTimeSeries, data)


# -----------------------------------------------------------------------------
def prepare_for_test():
    from onyx.core import Date, GetObj
    from agora.corelibs.unittest_utils import AddIfMissing
    import agora.system.ufo_currency as ufo_currency

    ufo_currency.prepare_for_test()

    AddIfMissing(CurrencyCross(Currency1="USD", Currency2="USD"))
    AddIfMissing(CurrencyCross(Currency1="EUR", Currency2="USD"))
    AddIfMissing(CurrencyCross(Currency1="GBP", Currency2="USD"))

    marks = {
        "USD/USD": 1.00,
        "EUR/USD": 1.15,
        "GBP/USD": 1.50,
    }

    for cross, value in marks.items():
        cross = GetObj(cross)
        cross.UpdateTimeSeries([Date.today(), value])

    return marks
