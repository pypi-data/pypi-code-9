import logging
from falconer.data import daos


class AbstractDAO(object):
    """
        Convenience DAO allowing easy access to the SQL Session.
    """

    @staticmethod
    def begin():
        """
            Starts a transaction.
        """
        session = AbstractDAO.get_session()
        if session:
            session.begin()
        else:
            AbstractDAO.__LOGGER.warn("No database/session configured for this request. Is that intentional?")

    @staticmethod
    def commit():
        """
            Commits the current transaction.
        """
        session = AbstractDAO.get_session()
        if session:
            session.commit()
        else:
            AbstractDAO.__LOGGER.warn("No database/session configured for this request. Is that intentional?")

    @staticmethod
    def rollback():
        """
            Rolls back the current transaction.
        """
        session = AbstractDAO.get_session()
        if session:
            session.rollback()
        else:
            AbstractDAO.__LOGGER.warn("No database/session configured for this request. Is that intentional?")

    @staticmethod
    def get_session():
        """
            Returns the SQLAlchemy session.

            @rtype: sqlalchemy.orm.session.Session
        """
        return daos.Session

    __LOGGER = logging.getLogger(__name__)
    """ Logger for this class """

    __slots__ = tuple()