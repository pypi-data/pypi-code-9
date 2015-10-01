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

from onyx.core import (GCurve, Interpolate, RDate, DateRange, Structure,
                       GetObj, AddObj, UpdateObj, ExistsInDatabase,
                       ObjDbTransaction, ObjNotFound,
                       EvalBlock, GetVal, SetVal)

from agora.system.ufo_portfolio import Portfolio
from agora.corelibs.trade_api import TradesBy

__all__ = [
    "get_historical",
    "pnl_by_long_short",
    "update_attribution_hierarchy",
    "stats_by_portfolio",
    "stats_by_container",
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
    add_fvol = fields.pop("fvol", False)
    add_var = fields.pop("var", False)
    add_aum = fields.pop("aum", False)
    add_nav = fields.pop("nav", False)

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
            if add_fvol:
                values["fvol"] = GetVal(port, "ForwardVol")
            if add_var:
                values["var"] = GetVal(port, "VaR")
            if add_aum and fund is not None:
                values["aum"] = GetVal(fund, "Aum")
            if add_nav and fund is not None:
                values["nav"] = GetVal(fund, "Nav")

        results[date] = values

    return results


# -----------------------------------------------------------------------------
def pnl_by_long_short(port, start, end):
    """
    Description:
        Return historical daily P&L for long and short positions of a given
        portfolio, using the delta approximation.
        NB: We use adjusted prices to include the effect of dividends and
            assume that all positions are finaced in local currency (so that
            there is FX risk on the daily P&L only).
    Inputs:
        port  - portfolio name
        start - start date
        end   - end date
    Returns:
        A GCurve of dictionaries with field values.
    """
    crv_start = start + RDate("-1w")

    def get_price(sec, date):
        crv = GetVal(sec, "GetCurve", crv_start, end, field="Close")
        mul = GetVal(sec, "Multiplier")
        return mul*Interpolate(crv, date)

    def get_fx_rate(sec, date):
        cross = "{0:3s}/USD".format(GetVal(sec, "Denominated"))
        crv = GetVal(cross, "GetCurve", crv_start, end)
        return Interpolate(crv, date)

    def get_pos_and_prices(port, date):
        with EvalBlock() as eb:
            eb.set_diddle("Database", "PricingDate", date)
            pos = GetVal(port, "Deltas")
        return pos, {sec: get_price(sec, date) for sec in pos}

    date = start + RDate("-1b")
    old_pos, old_prcs = get_pos_and_prices(port, date)
    results = GCurve()

    for date in DateRange(start, end, "+1b"):
        fx_rates = {sec: get_fx_rate(sec, date) for sec in old_pos}
        long = short = 0.0
        for sec, qty in old_pos.items():
            pnl = qty*(get_price(sec, date) - old_prcs[sec])*fx_rates[sec]
            if qty >= 0.0:
                long += pnl
            else:
                short += pnl

        results[date] = {"long": long, "short": short}

        old_pos, old_prcs = get_pos_and_prices(port, date)

    return results


# -----------------------------------------------------------------------------
def update_attribution_hierarchy(fund):
    """
    Description:
        Updates the equity attribution hierarchy for all books that are leafs
        of a given fund.
    Inputs:
        fund - the fund's name
    Returns:
        None
    """
    port = GetVal(fund, "Portfolio")
    books = GetVal(port, "Books")
    fund_ccy = GetVal(fund, "Denominated")

    with ObjDbTransaction("Rebuild hierarchy"):
        for container in ("Countries", "Regions", "Sectors", "Subsectors"):
            for bucket in GetVal(container, "Items"):
                name = "{0:s} {1:s}".format(port, bucket.upper())
                try:
                    SetVal(name, "Children", Structure())
                except ObjNotFound:
                    continue

        for book in books:
            assets = set()
            for trade in TradesBy(book=book):
                sec_traded = GetVal(trade, "SecurityTraded")
                try:
                    asset = GetVal(sec_traded, "Asset")
                except AttributeError:
                    continue
                else:
                    assets.add(asset)
            if not len(assets):
                continue    
            for attr in ("Country", "Region", "Sector", "Subsector"):
                buckets = {GetVal(asset, attr) for asset in assets}
                qty = 1.0 / float(len(buckets))
                for bucket_name in buckets:
                    name = "{0:s} {1:s}".format(port, bucket_name.upper())
                    try:
                        bucket = GetObj(name)
                    except ObjNotFound:
                        bucket = AddObj(Portfolio(Name=name,
                                                  DisplayName=bucket_name,
                                                  Denominated=fund_ccy))
                    children = bucket.Children or Structure()
                    children[book] = qty
                    bucket.Children = children
                    UpdateObj(bucket)


# -----------------------------------------------------------------------------
def stats_by_portfolio(fund, month):
    """
    Description:
        Return attribution statistics (Gross Exposure, Net Exposure, and MTD
        P&L) on a given month for all the children of a given fund.
    Inputs:
        fund  - the fund's name
        month - the month's date (usually the last day)
    Returns:
        A dictionary.
    """
    port = GetVal(fund, "Portfolio")
    start = month + RDate("-1m+e")
    end = month + RDate("+e")
    stats = {}

    with EvalBlock() as eb:
        eb.set_diddle("Database", "PricingDate", end)
        stats = {
            "date": end,
            "aum": GetVal(fund, "Aum"),
            "nav": GetVal(fund, "Nav"),
        }

    for kid in GetVal(port, "Children"):
        info = {}
        with EvalBlock() as eb:
            eb.set_diddle("Database", "PricingDate", start)
            mktval_start = GetVal(kid, "MktValUSD")
        with EvalBlock() as eb:
            eb.set_diddle("Database", "PricingDate", end)
            info["gross"] = GetVal(kid, "GrossExposure")
            info["net"] = GetVal(kid, "NetExposure")
            mktval_end = GetVal(kid, "MktValUSD")
        info["mtd pnl"] = mktval_end - mktval_start
        stats[GetVal(kid, "DisplayName")] = info

    return stats


# -----------------------------------------------------------------------------
def stats_by_container(container, fund, month):
    """
    Description:
        Return attribution statistics (Gross Exposure, Net Exposure, and MTD
        P&L) on a given month for all the portfolios in a given container.
    Inputs:
        container - the container's name
        fund      - the fund's name (used to get AUM)
        month     - the month's date (usually the last day)
    Returns:
        A dictionary.
    """
    port = GetVal(fund, "Portfolio")
    start = month + RDate("-1m+e")
    end = month + RDate("+e")
    stats = {}

    with EvalBlock() as eb:
        eb.set_diddle("Database", "PricingDate", end)
        stats = {
            "date": end,
            "aum": GetVal(fund, "Aum"),
            "nav": GetVal(fund, "Nav"),
        }

    for item in GetVal(container, "Items"):
        kid = "{0:s} {1:s}".format(port, item.upper())
        if not ExistsInDatabase(kid):
            continue
        info = {}
        with EvalBlock() as eb:
            eb.set_diddle("Database", "PricingDate", start)
            mktval_start = GetVal(kid, "MktValUSD")
        with EvalBlock() as eb:
            eb.set_diddle("Database", "PricingDate", end)
            info["gross"] = GetVal(kid, "GrossExposure")
            info["net"] = GetVal(kid, "NetExposure")
            mktval_end = GetVal(kid, "MktValUSD")
        info["mtd pnl"] = mktval_end - mktval_start
        stats[GetVal(kid, "DisplayName")] = info

    return stats
