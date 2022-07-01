import time

from flask import request, jsonify

from app import db
from app.api import api
from app.api.auth_token import auth
from app.modles import Wonnot, Customer, Light, Cailiao


@api.route('/api/dingdan', methods=['GET', 'POST'])
@auth.login_required
def getoder():
    list = []
    if request.method == 'GET':
        cus = Wonnot.query.all()
        for i in cus:
            list.append(i.to_json())
        return jsonify(list)
    elif request.method == 'POST':
        date = request.get_json(silent=True)['date']
        date = time.localtime(date / 1000)
        date = time.strftime('%Y-%m-%d', date)
        number = request.get_json(silent=True)['number']
        name = request.get_json(silent=True)['name']
        cus = Customer.query.filter(Customer.company == name)
        for i in cus:
            phone = i.phone
        cost = 0
        sales = request.get_json(silent=True)['sales']
        profit = 0
        s1 = Customer.query.filter((Customer.company == name) & (Customer.phone == phone))
        for i in s1:
            customer_id = i.id
        data = Wonnot(date=date, number=number, name=name, phone=phone, cost=cost, sales=sales, profit=profit,
                      customer_id=customer_id)
        db.session.add(data)
        db.session.commit()
        return '200'


@api.route('/api/dingdanpage', methods=['GET', 'POST'])
@auth.login_required()
def dingdanpage():
    if request.method == 'POST':
        id = request.get_json(silent=True)['id']
        if id == 1:
            pagesize = request.get_json(silent=True)['pagesize']
            page = request.get_json(silent=True)['page']
            reslist = []
            data = Wonnot.query.order_by(Wonnot.number.desc()).paginate(page, pagesize).items
            totalpage = Wonnot.query.count()
            for i in data:
                reslist.append(i.to_json())
            reslist.append({'totalpage': totalpage})
            return jsonify(reslist)

@api.route('/api/dingdan/<int:id>', methods=['DELETE', 'POST'])
@auth.login_required
def deloder(id):
    if request.method == 'DELETE':
        data = Light.query.filter(Light.oder_id == id)
        for i in data:
            Cailiao.query.filter(Cailiao.light_id == i.id).delete()
        Light.query.filter(Light.oder_id == id).delete()
        Wonnot.query.filter(Wonnot.id == id).delete()
        db.session.commit()
        return '200'
    if request.method == 'POST':
        number = request.get_json(silent=True)['number']
        name = request.get_json(silent=True)['name']
        data = Wonnot.query.get(id)
        data.number = number
        data.name = name
        data2 = Customer.query.filter(Customer.company == name).first()
        data.customer_id = data2.id
        db.session.commit()
        return {'code': 200}


@api.route('/api/dingdanview/<int:id>', methods=['GET'])
@auth.login_required
def view(id):
    list = []
    s = Customer.query.get(id)
    for i in s.oders:
        list.append(i.to_json())
    return jsonify(list)
