import jwt
import datetime
import app
from db import User
def create_session(user):
    njwt = jwt.encode({'username': user.username,
                       'paths': user.paths,
                       'exp': (datetime.datetime.now() + datetime.timedelta(hours=int(app.JWT_EXPIRES_HRS))),
                       'isadmin': user.isadmin
                       }, app.JWT_SECRET, algorithm='HS256')
    return njwt
def verify_session(token):
    try:
        u = jwt.decode(token, app.JWT_SECRET, algorithms=['HS256'])
        return User(u["username"], "", u["paths"], u["isadmin"])
    except Exception as e:
        print(e)
        return None