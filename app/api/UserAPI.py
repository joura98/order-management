from flask import request, jsonify
from app import db
from app.api import api
from app.modles import User, Role
from app.api.auth_token import auth


@api.route('/api/user', methods=['GET', 'POST'])
@auth.login_required()
def getuser():
    if request.method == 'GET':
        data = User.query.all()
        list = []
        for i in data:
            list.append(i.to_json())
        return jsonify(list)
    if request.method == 'POST':
        user = request.get_json(silent=True)['user']
        password = request.get_json(silent=True)['password']
        role = request.get_json(silent=True)['role']
        name = request.get_json(silent=True)['name']
        data = User(user=user, password=password, role=role, name=name)
        db.session.add(data)
        db.session.commit()
        return '200'


@api.route('/api/role', methods=['GET'])
@auth.login_required()
def getrole():
    data = Role.query.all()
    list = []
    for i in data:
        list.append(i.to_json())
    return jsonify(list)


@api.route('/api/user/<int:id>', methods=['DELETE', 'POST'])
@auth.login_required()
def deluser(id):
    if request.method == 'DELETE':
        User.query.filter(User.id == id).delete()
        db.session.commit()
        return '200'
    if request.method == 'POST':
        user = request.get_json(silent=True)['user']
        role = request.get_json(silent=True)['role']
        name = request.get_json(silent=True)['name']
        data = User.query.get(id)
        data.user = user
        data.role = role
        data.name = name
        db.session.commit()
        return '200'


@api.route('/api/editpassword', methods=['POST'])
@auth.login_required()
def editpassword():
    if request.method == 'POST':
        name = request.get_json(silent=True)['name']
        password = request.get_json(silent=True)['password']
        data = User.query.filter(User.name == name).first()
        data.password = password
        db.session.commit()
        return '200'


@api.route('/api/restpassword/<int:id>', methods=['POST'])
@auth.login_required()
def restpassword(id):
    if request.method == 'POST':
        data = User.query.get(id)
        data.password = '202cb962ac59075b964b07152d234b70'
        db.session.commit()
        return '200'
