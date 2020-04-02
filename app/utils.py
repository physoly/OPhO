import inspect
from functools import wraps
from sanic import response
import string
import random

def get_stack_variable(name):
    stack = inspect.stack()
    try:
        for frames in stack:
            try:
                frame = frames[0]
                current_locals = frame.f_locals
                if name in current_locals:
                    return current_locals[name]
            finally:
                del frame
    finally:
        del stack

def auth_required():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = request['session'].get('logged_in', False)
            if is_authorized:
                resp = await f(request, *args, **kwargs)
                return resp
            return response.redirect('/login')
        return decorated_function
    return decorator

def id_generator(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False