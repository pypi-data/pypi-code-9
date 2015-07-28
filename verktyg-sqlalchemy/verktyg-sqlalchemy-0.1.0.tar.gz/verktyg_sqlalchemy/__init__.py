from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from werkzeug.utils import cached_property


class SQLAlchemyApplicationMixin(object):
    @property
    def db_uri(self):
        return self.config['verktyg_sqlalchemy.database_uri']

    @cached_property
    def db_engine(self):
        return create_engine(self.db_uri)

    def db_make_session(self):
        return Session(bind=self.db_engine, expire_on_commit=False)

    @contextmanager
    def db_session(self):
        session = self._db_session_factory()

        try:
            yield session
            session.commit()
            session.expunge_all()
        except:
            session.rollback()
            raise
        finally:
            session.close()


class SQLAlchemyRequestMixin(object):
    @cached_property
    def db_session(self):
        session = self.app.db_make_session()

        def _close_session():
            try:
                session.rollback()
            finally:
                session.close()

        self.call_on_close(_close_session)
        return session


def bind(builder, *, database_uri):
    builder.config['verktyg_sqlalchemy.database_uri'] = database_uri

    builder.add_application_mixins(SQLAlchemyApplicationMixin)
    builder.add_request_mixins(SQLAlchemyRequestMixin)


__all__ = ['SQLAlchemyApplicationMixin', 'SQLAlchemyRequestMixin']
