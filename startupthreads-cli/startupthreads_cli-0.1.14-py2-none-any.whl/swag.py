#!/usr/bin/env python


""" View StartupThreads inventory/send t-shirts """

import json
import requests
import os
import click
import arrow
import getpass
from tabulate import tabulate

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda x: x.lower()
    )

TSHIRT_SIZES = ["MS", "MM", "ML", "MXL", "M2XL",
                "WS", "WM", "WL", "WXL", "W2XL"]


class RestAPI:
    def __init__(self, base_url, headers={}):
        self.url = base_url

    def get(self, params):

        click.secho("getting: {}... "
                    .format(self.url + params), fg='blue', nl=False)
        url = "{}".format(self.url + params)

        try:
            req = requests.get(self.url + params, headers=self.headers)
            if req.ok:
                click.secho("OK", fg='green')
                return json.loads(req.content)
            else:
                click.secho("NOK: {}".format(req.reason), fg='red')
                return {'error': req.content}
        except requests.exceptions.ConnectionError, m:
            click.secho("NOK (requests.exceptions.ConnectionError): {}"
                        .format(m), fg='red')
        except:
            click.secho("NOK, unknown", fg='red')

        raise RequestError("{} // {}/{}"
                           .format(url, req.status_code, req.reason))

    def post(self, data, params):
        """ send a POST request """
        url = "{}".format(self.url + params)
        click.secho("posting: {} ".format(url), fg='blue', nl=False)

        try:
            req = requests.request('post',
                                   url,
                                   json=data,
                                   headers=self.headers)

            if req.ok:
                click.secho("OK", fg='green')
                return json.loads(req.content)
            else:
                click.secho("NOK: {}".format(req.reason), fg='red')
                return json.loads(req.content)

        except requests.exceptions.ConnectionError, m:
            click.secho("NOK: {}".format(m), fg='red')

        raise RequestError("{} // {}/{}"
                           .format(url, req.status_code, req.reason))


class StartupThreadsAPI(RestAPI):

    def __init__(self, url):
        self.url = url

        self.check_token()
        self.key = os.environ.get('STARTUPTHREADS_API_KEY')
        self.cache = {}

        self.headers = {
            "Authorization": 'Token token="{}"'.format(self.key),
            'Accept': 'application/vnd.startupthreads-v1+json',
            }

        RestAPI.__init__(self, url, self.headers)

    def tshirt_ids(self):
        """ return a list of existing t-shirt IDs """
        inventory = self.inventory()
        return [item['id'] for item in inventory['items']]

    def check_token(self):
        if 'STARTUPTHREADS_API_KEY' not in os.environ:
            dashboard_url = "https://dashboard.startupthreads.com/"
            click.secho("No STARTUPTHREADS_API_KEY envvar found. ", fg='red')
            msg = ("Retrieve it from the StartupThreads dashboard:\n")
            msg += click.style(dashboard_url, fg='blue') + "\n"
            msg += ("Once you have it, add it to your bash profile: \n"
                    "export STARTUPTHREADS_API_KEY='changeme'")
            click.secho(msg)
            exit()

    def place_giveaway(self, order_info):
        """ create a new giveaway """
        params = "/giveaways/"
        return self.post(order_info, params)

    def place_order(self, order_info):
        """ place a new StartupThreads order"""

        params = "/inventory_shipments/"
        return self.post(order_info, params)

    def inventory(self):
        if 'inventory' in self.cache:
            return self.cache['inventory']
        self.cache['inventory'] = self.get("/items.json")
        return self.cache['inventory']

    def get_order_by_id(self, order_id):
        params = "/orders/" + order_id
        return self.get(params)

    def get_item_by_id(self, item_id):
        i = self.inventory()
        items = i['items']
        for x in items:
            if x['id'] == item_id:
                return x
        return {'error': '{} is not a valid item ID'}

    def prompt_for_tshirts(self):
        """ Prompt user for one or more t-shirt IDs"""
        default_item = self.inventory()['items'][0]

        msg = ("Item ID(s), separated by spaces (default is {}; "
               "type '?' to view the list)"
               .format(default_item['name']))
        answer = click.prompt(msg, default=default_item['id'])
        while answer not in self.tshirt_ids():
            if answer == '?':
                self.inventory_show(self.inventory())
            else:
                click.secho("Not a valid t-shirt ID: {}"
                            .format(answer), fg='red')
            answer = self.prompt_for_tshirts()
        return answer

    def inventory_show(self, inventory):
        """ Display our StartupThreads inventory """
        inventory = inventory['items']

        headers = ['name', 'id', 'status', 'description']
        headers.extend(TSHIRT_SIZES)
        headers.append('link')
        rows = []
        for item in inventory:
            row = [
                item['name'],
                item['id'],
                item['status'],
                item['description'],
            ]

            sizes = dict((size['size'], size['quantity'])
                         for size in item['inventory'])
            for s in TSHIRT_SIZES:
                row.append(sizes.get(s, ''))

            row.append(item['mockup'])  # this is a real long URL
            rows.append(row)

        table = tabulate(rows, headers)
        print(table)


class RequestError(Exception):
    pass


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option('-i', '--interactive', is_flag=True,
              help='place an order interactively')
@click.argument('email', required=False)
def giveaway(email, interactive):
    """ Create a new StartupThreads giveaway (i.e. send someone
    a link to redeem a free t-shirt)"""
    giveaway_submit(email, interactive)


@cli.command()
@click.option('-t', '--test', is_flag=True,
              help='Dry run/test mode')
@click.option('-i', '--interactive', is_flag=True,
              help='place an order interactively')
@click.argument('address', required=False)
def send(test, address, interactive):
    """ create a new StartupThreads order"""
    order_submit(address, interactive, test)


@cli.command()
@click.argument('order', required=True)
def status(order):
    """show the status of a StartupThreads order"""
    order_id = order
    order = THREADS.get_order_by_id(order_id)
    if 'error' in order:
        click.secho("Couldn't fetch order {}: "
                    .format(order_id), fg='red')
        click.secho(getattr(order['error'], "message", order['error']))
    else:
        click.secho(tabulate(order['order'].items(),
                             ['recipient']
                             ),
                    fg='green')


@cli.command()
def inventory(*args, **kwargs):
    """ Call a function to display our StartupThreads inventory"""
    inventory = THREADS.inventory()
    THREADS.inventory_show(inventory)


def giveaway_submit(recipients, interactive):
    """ give away a t-shirt via StartupThreads """

    if interactive or not recipients:
        default_name = getpass.getuser() + '-' + arrow.now().format('X')
        giveaway_name = click.prompt((
            "A name for this giveaway (must be unique; if you're not "
            "sure, just hit enter to accept the default value)"),
            default=default_name)
        item_ids = THREADS.prompt_for_tshirts().split()
        quantity = click.prompt(("Number of times this giveaway "
                                 "can be redeemed"), default=1)
        recipients = click.prompt("recipient email address(es)",
                                  default="aj@gandi.net")

    recipients = recipients.split()
    recipients.append('bot@gandi.community')

    # right now we can only submit one giveaway at a time, but StartupThreads
    # promises this should change soon
    for item_id in item_ids:
        order_info = {
            'giveaway': {
                'name': giveaway_name,
                'item_id': item_id,
                'payment_method': 'account_balance',
                'item_claim_limit': quantity,
                'emails': recipients,
                'us_only': False,
                'only_sizes_in_inventory': True}
            }

        # format order information for terminal display
        to_show = order_info['giveaway'].copy()
        to_show['emails'] = ", ".join(to_show['emails'])
        to_show['item name'] = THREADS.get_item_by_id(item_id)['name']
        to_show['item id'] = "{}".format(item_id)

        # display order summary; prompt user for confirmation before continuing
        click.secho(tabulate(to_show.items(), headers=['order info']),
                    fg='yellow')

        if not click.confirm(("This is not a test. Are you sure you want to "
                              "proceed?"), default=True):
            exit()

        order = THREADS.place_giveaway(order_info)

        if order:
            if any(['error' in order, 'errors' in order]):
                click.secho("ERROR(S):", fg='red')
                if 'errors' in order:
                    errors = order['errors']
                else:
                    errors = [order['error']]
                for x in errors:
                    click.echo(x)
                if 'data' in order:
                    print(order['data'])
                click.echo("The info provided:")
                click.echo(tabulate(order_info['giveaway'].items(),
                           headers=['value']))
            if 'giveaway' in order:
                click.secho("SUCCESS:", fg='green')
                print(order)
                order = order['giveaway']
                print(giveaway_status(order))
        else:
            print("Something went wrong with the order. Are you online?")


def giveaway_status(giveaway):
    # create a table showing startupthreads giveaway order status
    # fixme: this just doesn't work at all (404), maybe not supported?
    click.secho(("StartupThreads API doesn't support checking the status of "
                 "a giveaway yet, but here's the info we sent:"))

    giveaway['emails'] = ", ".join(giveaway['emails'])
    giveaway_id = giveaway['id']
    giveaway['url'] = ("https://dashboard.startupthreads.com"
                       "/giveaways/{}/claim"
                       .format(giveaway_id))
    table = tabulate(giveaway.items(), headers=[giveaway['name']])
    return table


def order_submit(address, interactive, test):
    # order a t-shirt

    if interactive or not address:
        item_id = THREADS.prompt_for_tshirts()
        size = click.prompt("Size", default="MM")
        quantity = click.prompt("Quantity", default=1)
        address = prompt_for_postal_address()

    order_info = {
        'inventory_shipment': {
            'payment_method': 'account_balance',
            'line_items': [
                {
                    'item_id': item_id,
                    'size': size,
                    'quantity': quantity
                }
            ],
            'address': address,
            'test_mode': test
        }
    }

    a = order_info['inventory_shipment']['address']
    click.secho("Sending {} {} size {} to:"
                .format(quantity, item_id, size), fg='blue')

    click.secho(tabulate(a.items(), headers=['recipient']), fg='yellow')

    if not test:
        if not click.confirm(default=True, fg='red'):
            exit()

    order = THREADS.place_order(order_info)

    if order:
        if 'error' in order.keys():
            click.secho("ERROR(S):", fg='red')
            errors = order['error'].split(',')
            for x in errors:
                click.echo(x)
            click.echo("the info provided:")
            click.echo(tabulate(order_info['inventory_shipment'].items(),
                       headers=['value']))
        else:
            click.secho("SUCCESS:", fg='green')
            o = order['inventory_shipment']
            a = o['address']
            del(o['address'])
            order_id = o['id']
            status([order_id])
    else:
        click.secho("Something went wrong with the order. Are you online?",
                    fg='red')


def prompt_for_postal_address():
    name = click.prompt("Recipient name",
                        default="AJ Bowen, c/o Gandi.net")
    street1 = click.prompt("Street1", default="121 2nd St")
    street2 = click.prompt("Street2", default="5th Fl")
    city = click.prompt("City", default="San Francisco")
    zip_code = click.prompt("Zip code", default="94105")
    state = click.prompt("State", default="CA")
    country = click.prompt("Country", default="US")

    address = {
        'name': name,
        'street1': street1,
        'street2': street2,
        'city': city,
        'state': state,
        'zip': zip_code,
        'country': country
    }

    return address

THREADS = StartupThreadsAPI('https://api.startupthreads.com')


if __name__ == '__main__':

    cli(obj={})
