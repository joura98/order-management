import json
import os
import uuid
from flask import jsonify, request
from app import db
from app.api import api
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.api.auth_token import auth
from app.modles import User, Light


@api.route('/api/uploadpicture/', methods=['PUT', 'POST', 'GET', 'DELETE'])
def uploadpicture():
    if request.method == 'POST':
        file = request.files['file']
        f = request.form.to_dict()
        id = f['id']
        token = f['token']
        s = Serializer('sdfFSDSDFfdas')
        data = s.loads(token)
        user = data['id']
        password = data['password']
        data2 = User.query.filter(User.user == user).first()
        if data2.password == password:
            basepath = os.getcwd() + '\\static\\image\\'
            dir_path = str(basepath) + str(id) + '\\'
            file_path = dir_path + str(uuid.uuid4()) + '.jpg'
            if os.path.exists(dir_path):
                file.save(file_path)
            else:
                os.makedirs(dir_path)
                file.save(file_path)
            s = []
            data = Light.query.get(id)
            for root, dirs, files in os.walk(dir_path):
                for i in files:
                    s.append('\\image\\' + str(id) + '\\' + i)
            data.image = json.dumps(s)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '上传成功'})
        else:
            return jsonify({'msg': '请不要乱搞'})
    if request.method == 'PUT':
        id = request.get_json(silent=True)['id']
        preview = request.get_json(silent=True)['preview']
        namelist = []
        basepath = os.path.abspath(os.path.join(os.getcwd(), 'static', 'image\\'))
        dir_path = os.path.join(basepath, str(id))
        for root, dirs, files in os.walk(dir_path):
            for i in files:
                namelist.append(i)
        count = 0
        list1 = []
        for i in namelist:
            if preview == 1:
                url = request.get_json(silent=True)['url']
                list1.append({'name': namelist[count], 'url': url + '\\image\\' + str(id) + '\\' + i})
                count += 1
            if preview == 2:
                count += 1
                list1.append({'id': count, 'url': i})
        return jsonify(list1)


@api.route('/api/delpicture/', methods=['PUT', 'POST', 'GET', 'DELETE'])
@auth.login_required()
def delpicture():
    if request.method == 'POST':
        baseurl = os.path.abspath(os.path.join(os.getcwd(), 'static', 'image\\'))
        id = request.get_json(silent=True)['id']
        name = request.get_json(silent=True)['name']
        delmulu = os.path.join(baseurl, str(id), name)
        os.remove(delmulu)
        data = Light.query.get(id)
        basepath = os.getcwd() + '\\static\\image\\'
        dir_path = str(basepath) + str(id) + '\\'
        s = []
        for root, dirs, files in os.walk(dir_path):
            for i in files:
                s.append('\\image\\' + str(id) + '\\' + i)
        data.image = json.dumps(s)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '删除成功'})
