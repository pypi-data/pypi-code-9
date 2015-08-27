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

from onyx.core import (Date, GetObj, ObjNamesByType, ObjNotFound,
                       UseGraph, GetVal, InvalidateNode, IsInstance)

import onyx.database as onyx_db

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape

import psycopg2
import functools
import json
import logging

__all__ = [
    "get_all_books",
    "get_all_portfolios",
    "ObjectsHandler",
    "FundHandler",
    "ValueTypeHandler",
    "RiskMonitorBase"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(name)-32s %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
def get_all_books():
    """
    Description:
        Return all books that are children of one of the existing funds.
    Yields:
        A generator
    """
    funds = ObjNamesByType("Fund")
    books = set()
    for fund in funds:
        fund = GetObj(fund, refresh=True)
        port = GetObj(fund.Portfolio, refresh=True)
        books.update(port.Books)
    return books 


# -----------------------------------------------------------------------------
def get_all_portfolios(port):
    """
    Description:
        Return all sub-portfolios that are children of an input portfolio.
    Inputs:
        port - the name of the top portfolio
    Yields:
        A generator
    """
    port = GetObj(port, refresh=True)
    for kid in port.Children:
        if IsInstance(kid, "Portfolio"):
            yield from get_all_portfolios(kid)
    yield port.Name


###############################################################################
class ObjectsHandler(tornado.web.RequestHandler):
    # -------------------------------------------------------------------------
    def get(self, obj_type=None):
        response = ObjNamesByType(obj_type)

        self.set_status(200)
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(response))


###############################################################################
class FundHandler(tornado.web.RequestHandler):
    # -------------------------------------------------------------------------
    def get(self, fund_name):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")

        fund_name = tornado.escape.url_unescape(fund_name)

        try:
            fund = GetObj(fund_name, refresh=True)
        except ObjNotFound as err:
            self.set_status(404)
            self.write(json.dumps(str(err)))
        else:
            with self.application.graph:
                portfolio = GetVal(fund.Name, "Portfolio")
                children = sorted(GetVal(portfolio, "Children").keys())
                children = [portfolio] + children

                response = {
                    "aum": GetVal(fund.Name, "Nav"),
                    "ccy": GetVal(fund.Name, "Denominated"),
                    "portfolios": children,
                }

            self.set_status(200)
            self.write(json.dumps(response))


###############################################################################
class ValueTypeHandler(tornado.web.RequestHandler):
    """
    This handler manages requests to the specified value type.
    """
    # -------------------------------------------------------------------------
    def initialize(self, value_type):
        self.vt = value_type

    # -------------------------------------------------------------------------
    def get(self, book):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")

        try:
            with self.application.graph:
                response = GetVal(tornado.escape.url_unescape(book), self.vt)
        except ObjNotFound as err:
            response = str(err)
            self.set_status(404)
        else:
            self.set_status(200)

        self.write(json.dumps(response))


###############################################################################
class RiskMonitorBase(tornado.web.Application):
    """
    Typical use will be as follows:

        with UseDatabase(dbname):
            app = RiskMonitorBase(handlers=[
                (r"/objects$", ObjectsHandler),
                (r"/objects/(\w+$)", ObjectsHandler),
                (r"/funds/(.+)", FundHandler),
                (r"/deltas/(.+)", ValueTypeHandler, {"value_type": "Deltas"}),
            ])

            http_server = tornado.httpserver.HTTPServer(app)
            http_server.listen(port, address="127.0.0.1")
            tornado.ioloop.IOLoop.instance().start()
    """
    # -------------------------------------------------------------------------
    def __init__(self, stop_at, handlers=None, **kwds):
        super().__init__(handlers, **kwds)

        # --- stopping time
        self.stop_at = stop_at

        # --- create an instance of the environment used by the risk server
        self.graph = UseGraph()

        self.conn = onyx_db.obj_clt.conn
        io_loop = tornado.ioloop.IOLoop.instance()

        # --- listen on one or more channels
        self.listen("poseffects")

        # --- handler
        handler = functools.partial(self.receive, callback=self.poseffects)

        # --- add event receiver to tornado's IOLoop
        io_loop.add_handler(self.conn.fileno(), handler, io_loop.READ)

        # --- initialize the set of books that are known children of the
        #     existing funds
        with self.graph:
            self.children = get_all_books()

        # --- check periodically if the scheduler needs to be stopped
        tornado.ioloop.PeriodicCallback(self.check_stop, 60000).start()

    # -------------------------------------------------------------------------
    def check_stop(self):
        if Date.now() > self.stop_at:
            tornado.ioloop.IOLoop.instance().stop()
            logger.info("server is being stopped")

    # -------------------------------------------------------------------------
    def listen(self, channel):
        curs = self.conn.cursor()
        curs.execute("LISTEN {0:s};".format(channel))

    # -------------------------------------------------------------------------
    def receive(self, fd, events, callback):
        state = self.conn.poll()
        if state == psycopg2.extensions.POLL_OK:
            if self.conn.notifies:
                callback(self.conn.notifies.pop())

    # -------------------------------------------------------------------------
    def poseffects(self, msg):
        if msg.channel == "poseffects":
            with self.graph:
                # --- on this channel, payload is the the name of the book
                #     affected by changed positions
                book = msg.payload
                # --- first invalidate the children of the affected book so
                #     that they get recalculated fetching new data from the
                #     backend
                InvalidateNode(book, "Children")
                # --- if the book is not in the cached set of children
                #     invalidate the Children VT across the whole portfolio
                #     hierarchy
                if book not in self.children:
                    self.children = get_all_books()
                    for fund in ObjNamesByType("Fund"):
                        fund_port = GetVal(fund, "Portfolio")
                        for port in set(get_all_portfolios(fund_port)):
                            # --- this triggers reloading the object from
                            #     the backend
                            GetObj(port, refresh=True)
                            # --- this triggers invalidation per se
                            InvalidateNode(port, "Children")

            logger.info("Children of '{0:s}' invalidated".format(msg.payload))
