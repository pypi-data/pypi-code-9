import traceback
import pickle
import sys
import os
from functools import wraps
from datetime import datetime

from bottle import request, error


class Ragool(object):
    """Error handler for bottle applications.
        Ragool handles request headers and it"s error traceback.
        To install Ragool use:
            r = Ragool(app)

    """

    def __init__(self, bottle_app, path=None, install_route=None):
        """Ragool initializing function
            :param bottle_app:
                Bottle application to install Ragool at

            :param path:
                Path where Ragool stores it"s error files

                If no path given it will create directory
                "ragool" in current directory to store its files

            :param install_route:
                Base route to mount RagoolView app.
                RagoolView is a web interface for Ragool.
                Do not change this param if you want run it as standalone app.

        """
        if not path:
            self.path = os.path.dirname(
                os.path.realpath(sys.argv[0]))+"/ragool"
        else:
            self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.__bottle_app = bottle_app

        if install_route:
            from Ragool.ragool_view import RagoolView

            ragool_view_app = RagoolView()
            self.__bottle_app.mount(install_route, ragool_view_app)

    def install(self):
        self.__bottle_app.install(self.handle_error)

    def handle_error(self, request_handler):
        """Request handler for bottle app"""

        @wraps(request_handler)
        def wrapper(*args, **kwargs):
            try:
                return request_handler(*args, **kwargs)
            except Exception as e:
                err = {
                    "date": datetime.now(),
                    "headers": self.get_request_headers(request),
                    "traceback": {
                        "type": sys.exc_info()[0],
                        "value": sys.exc_info()[1],
                        "full": traceback.extract_tb(sys.exc_info()[2])
                    }
                }
                self.store_error(err)
                return error(500)
        return wrapper

    def store_error(self, err):
        """Pickles error message to file.
            File format is DAY_MONTH_HOUR_MINUTE_SECOND

            :param err:
               Dict containing date, request headers and traceback info.

        """
        timestamp = datetime.now().strftime("%d_%m_%H_%M_%S")
        with open("{}/{}".format(self.path, timestamp), "wb") as f:
            pickle.dump(err, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    def get_request_headers(self, request_):
        """Parses request headers to simple dict
            and adds additional information

            :param request_:
                Bottle request object to be parsed

        """

        request_data = {x: request_.headers[x] for x in request_.headers}
        request_data["path"] = request_.path
        request_data["remote-address"] = request_.remote_addr
        return request_data