from io import BytesIO
from flask import request, jsonify, make_response
import redis
from app.api import api
from app.modles import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from libs.Captcha import Captcha


@api.route('/api/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.get_json(silent=True)['user']
        password = request.get_json(silent=True)['password']
        code = request.get_json(silent=True)['code']
        if check_code(code) == 1:
            data = User.query.filter(User.user == user).first()
            list = []
            if data.password == password:
                s = Serializer('sdfFSDSDFfdas', expires_in=8 * 3600)
                token = s.dumps({"id": user, 'password': password}).decode("ascii")
                list.append(data.to_json())
                list.append({'token': token})
                return jsonify(list)
            else:
                return jsonify({'code': 403})
        else:
            return jsonify({'code': 402})


@api.route('/api/yanzheng')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    save_redis(text)
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    return resp


def connect_redis():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    return redis.Redis(connection_pool=pool)


def save_redis(code):
    rd = connect_redis()
    rd.set('code_' + code, code)  # 把验证码存储起来
    rd.expire('code_' + code, 60)  # 验证码 1分钟后失效


def check_code(code):
    rd = connect_redis()
    s = 1
    if not rd.get('code_' + code):
        s = 0
    return s
