from flask import request, jsonify
from app import db
from app.api import api
from app.api.auth_token import auth
from app.modles import Supplier


@api.route('/api/supplier', methods=['GET', 'POST'])
@auth.login_required
def getsupplier():
    if request.method == 'GET':
        data = Supplier.query.order_by(Supplier.company)
        list = []
        for i in data:
            list.append(i.to_json())
        return jsonify(list)
    elif request.method == 'POST':
        company = request.get_json(silent=True)['company']
        name = request.get_json(silent=True)['name']
        local = request.get_json(silent=True)['local']
        phone = request.get_json(silent=True)['phone']
        sort = request.get_json(silent=True)['sort']
        data = Supplier(company=company, name=name, local=local, phone=phone, sort=sort)
        db.session.add(data)
        db.session.commit()
        return '200'


@api.route('/api/supplierpage', methods=['GET', 'POST'])
@auth.login_required
def supplierpage():
    if request.method == 'POST':
        page = request.get_json(silent=True)['page']
        cus = Supplier.query.order_by(Supplier.company).paginate(page, 10).items
        list = []
        pagenumber = Supplier.query.count()
        for i in cus:
            list.append(i.to_json())
        if (pagenumber > 10) & (page == 1):
            list.append({'pagenumber': pagenumber})
        return jsonify(list)


@api.route('/api/supplier/<int:id>', methods=['DELETE', 'POST'])
@auth.login_required
def delsupplier(id):
    if request.method == 'DELETE':
        Supplier.query.filter(Supplier.id == id).delete()
        db.session.commit()
        return '200'
    if request.method == 'POST':
        company = request.get_json(silent=True)['company']
        name = request.get_json(silent=True)['name']
        local = request.get_json(silent=True)['local']
        phone = request.get_json(silent=True)['phone']
        sort = request.get_json(silent=True)['sort']
        data = Supplier.query.get(id)
        for i in data.cailiaos:
            i.csupplier = company
        data.company = company
        data.name = name
        data.local = local
        data.phone = phone
        data.sort = sort
        db.session.commit()
        return '200'
