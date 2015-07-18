import logging
import falcon
from falconer.data.daos.abstract_dao import AbstractDAO


class FalconExceptions(object):

    @staticmethod
    def handle_exception(ex, req, resp, params):
        """
            Rolls back the current transaction if an error has occurred
        """
        try:
            AbstractDAO.rollback()
        except Exception as _ex:
            ex = _ex

        FalconExceptions.__LOGGER.error("Error", exc_info=1)

        if not isinstance(ex, falcon.HTTPError):
            raise falcon.HTTPInternalServerError("Internal Error", str(ex))
        else:
            raise

    __LOGGER = logging.getLogger(__name__)