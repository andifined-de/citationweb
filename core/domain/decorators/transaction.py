import contextvars
from functools import wraps
from domain.connection import SessionLocal

# Context variable to save the db session
session_context = contextvars.ContextVar("db_session", default=None)


def transactional(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        session = session_context.get()
        # If we don't have a session in context yet, we have to create it
        if session is None:
            session = SessionLocal()
            session_context.set(session)
            # Once we have a session in our context
            # we can call the wrapped function and
            # commit after it's finished
            try:
                result = func(*args, **kwargs)
                session.commit()
            # If an exception ocures during the method
            # execution it won't be commited but will
            # be rolled back instead but we still need
            # to raise the exception cause it's not
            # ours to handle
            except Exception as e:
                session.rollback()
                raise
            # In the end we should close the session
            # and empty the context
            finally:
                session.close()
                session_context.set(None)
        # If we already have a session in context
        # than it means that this method is called
        # from already a transactional method which
        # will handle rollback so we won't need
        # to worry about it
        else:
            return func(*args, **kwargs)
        return result

    return wrap_func


def db(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        session = session_context.get()
        return func(*args, **kwargs, db=session)
    return wrap_func
