#!/usr/bin/env python
# encoding: utf-8


class Event(object):
    def __init__(self):
        self.__handlers = set()

    def __iadd__(self, handler):
        self.__handlers.add(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.discard(handler)
        return self

    def fire(self, *args, **kwargs):
        for handler in self.__handlers:
            handler(*args, **kwargs)

    def clear(self):
        self.__init__()

    def clear_obj_handler(self, obj):
        self.__handlers = [h for h in self.__handlers if h.__self__ != obj]


def tick_to_dict(tick):
    return {'exchange': tick.exchange,
            'sec_id': tick.sec_id,
            'utc_time': tick.utc_time,
            'last_price': tick.last_price,
            'open': tick.open,
            'high': tick.high,
            'low': tick.low,
            'cum_volume': tick.cum_volume,
            'cum_amount': tick.cum_amount,
            'cum_position': tick.cum_position,
            'last_amount': tick.last_amount,
            'last_volume': tick.last_volume,
            'upper_limit': tick.upper_limit,
            'lower_limit': tick.lower_limit,
            'settle_price': tick.settle_price,
            'trade_type': tick.trade_type,
            'pre_close': tick.pre_close,
            'bids': tick.bids,
            'asks': tick.asks}


def bar_to_dict(bar):
    return {'exchange': bar.exchange,
            'sec_id': bar.sec_id,
            'bar_time': bar.bar_time,
            'bar_type': bar.bar_type,
            'utc_time': bar.utc_time,
            'open': bar.open,
            'close': bar.clost,
            'high': bar.high,
            'low': bar.low,
            'volume': bar.volume,
            'amount': bar.amount,
            'pre_close': bar.pre_close,
            'flag': bar.flag,
            'adj_factor': bar.adj_factor}


def dailybar_to_dict(db):
    return {'exchange': db.exchange,
            'sec_id': db.sec_id,
            'bar_type': db.bar_type,
            'bar_time': db.bar_time,
            'open': db.open,
            'close': db.close,
            'high': db.high,
            'low': db.low,
            'volume': db.volume,
            'amount': db.amount,
            'position': db.position,
            'settle_price': db.settle_price,
            'upper_limit': db.upper_limit,
            'lower_limit': db.lower_limit,
            'pre_close': db.pre_close,
            'flag': db.flag,
            'adj_factor': db.adj_factor}


def order_to_dict(o):
    return {'strategy_id': o.strategy_id,
            'account_id': o.account_id,
            'cl_ord_id': o.cl_ord_id,
            'ex_ord_id': o.ex_ord_id,
            'exchange': o.exchange,
            'sec_id': o.sec_id,
            'position_effect': o.position_effect,
            'side': o.side,
            'order_type': o.order_type,
            'order_src': o.order_src,
            'status': o.status,
            'ord_rej_reason': o.ord_rej_reason,
            'ord_rej_reason_detail': o.ord_rej_reason_detail,
            'price': o.price,
            'volume': o.volume,
            'filled_vwap': o.filled_vwap,
            'filled_volume': o.filled_volume,
            'filled_amount': o.filled_amount,
            'sending_time': o.sending_time,
            'transact_time': o.transact_time,
            'stop_price': o.stop_price}


def execrpt_to_dict(e):
    return {'strategy_id': e.strategy_id,
            'cl_ord_id': e.cl_ord_id,
            'order_id': e.order_id,
            'exec_id': e.exec_id,
            'exchange': e.exchange,
            'sec_id': e.sec_id,
            'position_effect': e.position_effect,
            'side': e.side,
            'ord_rej_reason': e.ord_rej_reason,
            'ord_rej_reason_detail': e.ord_rej_reason_detail,
            'exec_type': e.exec_type,
            'price': e.price,
            'volume': e.volume,
            'amount': e.amount,
            'transact_time': e.transact_time}


def cash_to_dict(c):
    return {'strategy_id': c.strategy_id,
            'currency': c.currency,
            'nav': c.nav,
            'fpnl': c.fpnl,
            'pnl': c.pnl,
            'profit_ratio': c.profit_ratio,
            'frozen': c.frozen,
            'order_frozen': c.order_frozen,
            'available': c.available,
            'cum_inout': c.cum_inout,
            'cum_trade': c.cum_trade,
            'cum_pnl': c.cum_pnl,
            'cum_commission': c.cum_commission,
            'last_trade': c.last_trade,
            'last_pnl': c.last_pnl,
            'last_commission': c.last_commission,
            'last_inout': c.last_inout,
            'change_reason': c.change_reason,
            'transact_time': c.transact_time}


def position_to_dict(p):
    return {'strategy_id': p.strategy_id,
            'exhange': p.exchange,
            'sec_id': p.sec_id,
            'side': p.side,
            'volume': p.volume,
            'volume_today': p.volume_today,
            'vwap': p.vwap,
            'price': p.price,
            'fpnl': p.fpnl,
            'cost': p.cost,
            'order_frozen': p.order_frozen,
            'available': p.available,
            'last_price': p.last_price,
            'last_volume': p.last_volume,
            'init_time': p.init_time,
            'transact_time': p.transact_time}


def indicator_to_dict(i):
    return {'strategy_id': i.strategy_id,
            'account_id': i.account_id,
            'nav': i.nav,
            'pnl': i.pnl,
            'profit_ratio': i.profit_ratio,
            'sharp_ratio': i.sharp_ratio,
            'risk_ratio': i.risk_ratio,
            'trade_count': i.trade_count,
            'win_count': i.win_count,
            'lose_count': i.lose_count,
            'win_ratio': i.win_ratio,
            'max_profit': i.max_profit,
            'min_profit': i.min_profit,
            'max_single_trade_profit': i.max_single_trade_profit,
            'min_single_trade_profit': i.min_single_trade_profit,
            'daily_max_single_trade_profit': i.daily_max_single_trade_profit,
            'daily_min_single_trade_profit': i.daily_min_single_trade_profit,
            'max_position_value': i.max_position_value,
            'min_position_value': i.min_position_value,
            'max_drawdown': i.max_drawdown,
            'daily_pnl': i.daily_pnl,
            'daily_return': i.daily_return,
            'annual_return': i.annual_return,
            'transact_time': i.transact_time}
