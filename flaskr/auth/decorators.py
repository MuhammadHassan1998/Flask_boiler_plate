from flask import abort, session

def user_required(f):
    def decorator(*args, **kwargs):
        try:
            user = session['email']
            return f(*args, **kwargs)
        except:
            abort(401)
    return decorator