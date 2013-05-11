import model

def with_session(commit = False):
    def decorator(fn):
        def wrapped(*args, **kwargs):
            session = model.Session()
            ret = fn(*args, session = session, **kwargs)
            if commit:
                session.commit()
            else:
                session.close()
            return ret
        return wrapped
    return decorator
