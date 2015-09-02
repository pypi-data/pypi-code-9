__author__ = 'mkoponen'

from intrazon import *
import signal
import sys
import atexit


def signal_handler(signal, frame):
    if iz is not None:
        iz.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


@atexit.register
def exit_handler():
    if iz is not None:
        iz.stop()

command = None
app_key = None
app_auth_key = None
virtual_good_key = None
cc_name = None
cc_num = None
cc_csc = None
cc_exp_month = None
cc_exp_year = None

iz = None


def handle_cmdline_args():
    num_args = len(sys.argv)

    global command
    global app_key
    global app_auth_key
    global virtual_good_key
    global cc_name
    global cc_num
    global cc_csc
    global cc_exp_month
    global cc_exp_year

    command = sys.argv[1]
    app_key = sys.argv[2]
    app_auth_key = sys.argv[3]

    if num_args >= 5:
        virtual_good_key = sys.argv[4]
    else:
        virtual_good_key = None

    if num_args >= 6:
        cc_name = sys.argv[5]
    else:
        cc_name = "John Doe"
    if num_args >= 7:
        cc_num = sys.argv[6]
    else:
        # Test credit card accepted by Stripe in test mode
        cc_num = "4012888888881881"
    if num_args >= 8:
        cc_csc = sys.argv[7]
    else:
        cc_csc = "123"

    if num_args >= 9:
        cc_exp_month = sys.argv[8]
    else:
        cc_exp_month = "01"
    if num_args >= 10:
        cc_exp_year = sys.argv[9]
    else:
        cc_exp_year = "2050"


def main():
    global iz
    handle_cmdline_args()

    # Note that if you make this non-blocking, you have to redesign the callback functions in such a way that the next
    # step of the process will happen only after the previous step has been finished. This is why blocking mode is
    # simpler to use.
    iz = IntraZon(app_key, app_auth_key, nonblocking=False)

    if command == "listgoods":
        iz.virtual_goods(callb_list_virtual_goods)
    else:
        player = iz.add_player(callb_player_added, cc_name)

        if player is None:
            print "Failed to add player, exiting"
            exit()
        else:
            print "Key of new player: %s" % player.key

        # Player needs to be completely added before you call this line
        iz.register_payment_method(callback=callb_payment_method_added, player_key=player.key, cc_num=cc_num,
                                   cc_csc=cc_csc, cc_name=cc_name, cc_exp_month=cc_exp_month, cc_exp_year=cc_exp_year)

        # Payment method must be completely registered before you call this line
        if virtual_good_key is not None:
            iz.purchase_virtual_good(callback=callb_virtualgood_purchased, player_key=player.key,
                                     virtual_good_key=virtual_good_key)


def callb_player_added(player, error):
    if error is not None:
        print "Error in player_added(): %s" % error.message
        return None
    return player.key


def callb_payment_method_added(payment_method, error):
    if error is not None:
        print "Error in payment_method_added(): %s" % error.message
        return
    print "Successfully added Payment method; card holder name: %s" % (payment_method.cc_name)


def callb_virtualgood_purchased(virtual_good_purchase, error):
    if error is not None:
        print "Error in callb_virtualgood_purchased(): %s" % error.message
        return
    print "Successfully purchased virtual good with key %s for player with key %s" % \
          (virtual_good_purchase.virtual_good_key, virtual_good_purchase.player_key)


def callb_list_virtual_goods(virtual_goods, error):
    if error is not None:
        print "Error in callb_list_virtual_goods(): %s" % error.message
        return
    for virtual_good in virtual_goods:
        print "Name: %s" % virtual_good.name
        print "Key: %s" % virtual_good.key
        price = "N/A"
        if virtual_good.price is not None:
            price = "%d" % virtual_good.price
        print "Price in coins: %s" % price
        price = "N/A"
        if virtual_good.price_usd is not None:
            price = virtual_good.price_usd
        print "Price in USD: %s" % price
        price = "N/A"
        if virtual_good.price_eur is not None:
            price = virtual_good.price_eur
        print "Price in EUR: %s" % price
        thumbnail = "N/A"
        if virtual_good.thumbnail is not None:
            thumbnail = virtual_good.thumbnail
        print "Thumbnail URL: %s%s" % (IntraZon.INTRAZON_DOMAIN, thumbnail)
        sub_discount = "N/A"
        if virtual_good.subscriber_discount is not None:
            sub_discount = virtual_good.subscriber_discount
        print "Subscriber discount: %s %%" % sub_discount
        print "\n------------\n"

if __name__ == '__main__':
    if len(sys.argv) < 4 or sys.argv[1] != "listgoods" and sys.argv[1] != "newplayerpurchase":
        print \
            "Usage: python example.py listgoods|newplayerpurchase app_key auth_key [virtual_good_key] [player_name] \n"\
            "[cc_num] [cc_csc] [cc_exp_month] [cc_exp_year]\n\n"\
            "You can see your application's virtual goods by giving \"listgoods\" as first parameter, and the key\n" \
            "and authorization API key for the application.\n\n"\
            "Or you can create a new player, attach payment method info to it, and finally purchase a Virtual Good\n"\
            "(optional) by giving \"newplayerpurchase\" as first parameter, app and auth keys, and the key of the\n"\
            "Virtual Good you wish to purchase. Finally, you can give the credit card information. If you leave the\n"\
            "credit card parameters out, a test credit card will be used, which will work if your application is in\n"\
            "test mode. No real monetary transaction will be made, but the charge will be visible in IntraZon test\n"\
            "payment history.\n\n"\
            "If you do not give virtual_good_key, then the player will be created and the credit card information\n"\
            "added, but no purchase will be made."
    else:
        main()