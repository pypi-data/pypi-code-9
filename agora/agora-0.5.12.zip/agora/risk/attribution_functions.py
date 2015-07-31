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

from onyx.core import GCurve, DateRange, Interpolate, EvalBlock, GetVal

__all__ = [
    "get_historical",
    "pnl_by_long_short",
]


# -----------------------------------------------------------------------------
def get_historical(port, start, end, fields, fund=None):
    """
    Description:
        Get historical values for a given portfolio.
    Inputs:
        port   - portfolio name
        start  - start date
        end    - end date
        fields - a list of fields
        fund   - this field must specify the fund's name whenever aum is one
                 of the required fields
    Returns:
        A GCurve of dictionaries with field values.
    """
    fields = dict.fromkeys(fields, True)

    add_mktval = fields.pop("mktval", False)
    add_gross = fields.pop("gross", False)
    add_net = fields.pop("net", False)
    add_aum = fields.pop("aum", False)

    if len(fields):
        raise ValueError("Unrecognized fields: {0!s}".format(fields))

    results = GCurve()
    for date in DateRange(start, end, "+1b"):
        values = {}
        with EvalBlock() as eb:
            # --- this shifts back both market and positions
            eb.set_diddle("Database", "PricingDate", date)
            if add_mktval:
                values["mktval"] = GetVal(port, "MktValUSD")
            if add_gross:
                values["gross"] = GetVal(port, "GrossExposure")
            if add_net:
                values["net"] = GetVal(port, "NetExposure")
            if add_aum and fund is not None:
                values["aum"] = GetVal(fund, "Nav")

        results[date] = values

    return results


# -----------------------------------------------------------------------------
def pnl_by_long_short(port, start, end):
    """
    Description:
        Return historical daily P&L for long and short positions of a given
        portfolio, using the delta approximation.
        NB: We use adjusted prices to include the effect of dividends.
    Inputs:
        port  - portfolio name
        start - start date
        end   - end date
    Returns:
        A GCurve of dictionaries with field values.
    """
    def get_prc(sec, date):
        crv = GetVal(sec, "GetCurve", start, end, field="Close")
        mul = GetVal(sec, "Multiplier")
        cross = "{0:3s}/USD".format(GetVal(sec, "Denominated"))
        return mul*Interpolate(crv, date)*GetVal(cross, "Spot")

    date = start
    with EvalBlock() as eb:
        eb.set_diddle("Database", "PositionsDate", date)
        old_pos = GetVal(port, "Deltas")
    old_prcs = {sec: get_prc(sec, date) for sec in old_pos}

    results = GCurve()
    for date in DateRange(start, end, "+1b"):

        long = short = 0.0
        for sec, qty in old_pos.items():
            if qty >= 0.0:
                long += qty*(get_prc(sec, date) - old_prcs[sec])
            else:
                short += qty*(get_prc(sec, date) - old_prcs[sec])

        with EvalBlock() as eb:
            eb.set_diddle("Database", "PositionsDate", date)
            old_pos = GetVal(port, "Deltas")
        old_prcs = {sec: get_prc(sec, date) for sec in old_pos}

        results[date] = {"long": long, "short": short}

    return results
