from pyramda import curry


@curry
def with_session_from(make_session, f):
    session = make_session()
    try:
        result = f(session)
        session.commit()
        return result
    except:
        session.rollback()
        raise
    finally:
        session.close()
