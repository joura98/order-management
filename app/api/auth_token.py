from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.modles import User
auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    s = Serializer('sdfFSDSDFfdas')
    try:
        data = s.loads(token)
        user = data['id']
        password = data['password']
        data2 = User.query.filter(User.user == user).first()
        if data2.password == password:
            return True
        else:
            return None
    except Exception:
        return None
