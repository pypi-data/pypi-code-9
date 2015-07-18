import falcon
from falconer.data.daos.abstract_dao import AbstractDAO


class DAOTransactionMiddleware(object):
    """

    """
    def process_request(self, req, resp):
        """
            Processes the request before routing it and starts a database
            transaction.
        """
        AbstractDAO.begin()

    def process_response(self, req, resp, resource):
        """
            Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
        """
        if resp.status in DAOTransactionMiddleware.__OK_STATUSES:
            AbstractDAO.commit()
        else:
            assert resp.status not in DAOTransactionMiddleware.__OK_STATUSES
            AbstractDAO.rollback()

    __OK_STATUSES = frozenset([
        falcon.HTTP_100,
        falcon.HTTP_101,
        falcon.HTTP_200,
        falcon.HTTP_201,
        falcon.HTTP_202,
        falcon.HTTP_203,
        falcon.HTTP_204,
        falcon.HTTP_205,
        falcon.HTTP_206,
        falcon.HTTP_226,
        falcon.HTTP_300,
        falcon.HTTP_301,
        falcon.HTTP_302,
        falcon.HTTP_303,
        falcon.HTTP_304,
        falcon.HTTP_305,
        falcon.HTTP_307,
    ])
    """ List of all successful HTTP statuses """