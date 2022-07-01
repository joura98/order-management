from flask import request, jsonify
from app import db
from app.api import api
from app.api.auth_token import auth
from app.modles import Customer


@api.route('/api/customer', methods=['GET', 'POST'])
@auth.login_required
def customer():
    list = []
    if request.method == 'GET':
        cus = Customer.query.all()
        for i in cus:
            list.append(i.to_json())
        return jsonify(list)
    elif request.method == 'POST':
        companyname = request.get_json(silent=True)['companyname']
        name = request.get_json(silent=True)['name']
        local = request.get_json(silent=True)['local']
        phone = request.get_json(silent=True)['phone']
        data = Customer(company=companyname, name=name, local=local, phone=phone)
        db.session.add(data)
        db.session.commit()
        return '200'

@api.route('/api/customer/<int:id>', methods=['DELETE', 'POST'])
@auth.login_required
def delcustomer(id):
    if request.method == 'DELETE':
        Customer.query.filter(id == Customer.id).delete()
        db.session.commit()
        return '200'
    elif request.method == 'POST':
        Customer.edit(id)
        return '200'

@api.route('/api/customerpage', methods=['POST'])
@auth.login_required
def customerpage():
    if request.method == 'POST':
        page = request.get_json(silent=True)['page']
        pagetotal = Customer.query.count()
        data = Customer.query.paginate(page, 10).items
        res = []
        for i in data:
            res.append(i.to_json())
        if (page == 1) & (pagetotal > 10):
            res.append({'page': pagetotal})
        return jsonify(res)

