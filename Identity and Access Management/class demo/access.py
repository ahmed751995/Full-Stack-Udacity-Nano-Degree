from flask import Flask, request, abort
from functools import wraps

app = Flask(__name__)

def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)

    auth_header = request.headers['Authorization'].split(' ')
        
    if len(auth_header) != 2:
        abort(401)

    elif auth_header[0].lower() != 'bearer':
        abort(401)

    return auth_header[1]


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth_header()
        return f(jwt, *args, **kwargs)
    return wrapper
    

@app.route('/request')
@require_auth
def headers(jwt):
    print(jwt)
    print(name)
    return 'not implemented'
