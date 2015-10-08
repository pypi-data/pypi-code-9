# -*- coding:utf-8 -*-

# import sys
#
# sys.path.append('../src/')

from wechatpay import WechatPay


class Pay(WechatPay):
    appid = 'wxe2d40b8c9da51c4b'
    appSecret = 'bdb785fbd9c121da0c1036eb5af621f0'
    partnerKey = '6b87d3121e11b9a0a5e7ca374ecab558'
    notify_url = 'http://vacation.breadtrip.com/payment/wxpay/wap/notify/'
    mch_id = '1238366001'


def main():
    params = {
        'body': '测试订单',
        'out_trade_no': 'local123123124123291',
        'total_fee': 1,
        'fee_type': 'CNY',
        'spbill_create_ip': '127.0.0.1',
        'product_id': 123123123,
    }
    print Pay().qrcode_pay(params)
    return

if __name__ == "__main__":
    main()
