from collections import Counter
from flask import request, jsonify
from app import db
from app.api import api
from app.api.auth_token import auth
from app.modles import Customer, Wonnot, User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@api.route('/api/zhanshi', methods=['GET', 'POST', 'PUT'])
@auth.login_required()
def zhanshi():
    if request.method == 'GET':
        data = db.session.query(Wonnot.sales, Wonnot.profit)
        s = 0
        s1 = 0
        for i in data:
            s = float('%.2f' % (s + i.sales))
            s1 = float('%.2f' % (s1 + i.profit))
        data1 = Wonnot.query.count()
        data2 = Customer.query.count()
        return jsonify({'number': s, 'totalprofit': s1, 'cusnumber': data2, 'ordernumber': data1})
    if request.method == 'POST':
        data = Wonnot.query.order_by(Wonnot.sales.desc()).limit(5)
        list = []
        for i in data:
            list.append([i.number, i.sales, i.cost, i.profit])
        return jsonify({'total': list})
    if request.method == 'PUT':
        data = db.session.query(Wonnot.customer_id)
        list = []
        for i in data:
            list.append(i.customer_id)
        list2 = Counter(list).most_common(10)
        list3 = []
        for i in list2:
            data1 = Customer.query.filter(Customer.id == i[0]).first()
            list3.append({'name': data1.company, 'value': i[1]})
        return jsonify(list3)


@api.route('/api/zhanshitotal', methods=['GET'])
@auth.login_required()
def zhanshitotal():
    if request.method == 'GET':
        data = db.session.query(Wonnot.customer_id)
        list = []
        for i in data:
            list.append(i.customer_id)
        list2 = Counter(list).most_common(10)
        list3 = []
        for i in list2:
            data1 = Customer.query.filter(Customer.id == i[0]).first()
            s = 0
            s1 = 0
            s2 = 0
            for k in data1.oders:
                s = float('%.2f' % (s + k.sales))
                s1 = float('%.2f' % (s1 + k.cost))
                s2 = float('%.2f' % (s2 + k.profit))
            list3.append([data1.company, s, s1, s2])
        list3.insert(0, ['product', '客户订单总额', '客户订单成本', '客户订单利润'])
        return jsonify(list3)


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
