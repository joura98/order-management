from flask import request, jsonify

from app import db
from app.api import api
from app.api.auth_token import auth
from app.modles import Light, Wonnot, Cailiao


@api.route('/api/light', methods=['GET', 'POST'])
@auth.login_required
def getlight():
    list = []
    if request.method == 'GET':
        data = Light.query.all()
        for i in data:
            list.append(i.to_json())
        return jsonify(list)
    if request.method == 'POST':
        ltype = request.get_json(silent=True)['ltype']
        lsort = request.get_json(silent=True)['lsort']
        lcolor = request.get_json(silent=True)['lcolor']
        lcount = request.get_json(silent=True)['lcount']
        lsize = request.get_json(silent=True)['lsize']
        lcost = 0
        lprice = request.get_json(silent=True)['lprice']
        oder_id = request.get_json(silent=True)['oder_id']
        data = Light(ltype=ltype, lsort=lsort, lcolor=lcolor, lcount=lcount,
                     lsize=lsize, lcost=lcost, lprice=lprice, oder_id=oder_id)
        db.session.add(data)
        db.session.commit()
        totaldingdan(oder_id)
        return '200'


@api.route('/api/light/<int:id>', methods=['GET', 'DELETE', 'POST'])
@auth.login_required
def getorderlight(id):
    if request.method == 'GET':
        list = []
        data = Wonnot.query.get(id)
        for i in data.lights:
            list.append(i.to_json())
        return jsonify(list)
    elif request.method == 'DELETE':
        data = Light.query.get(id)
        for i in data.cailiaos:
            Cailiao.query.filter(Cailiao.light_id == i.id).delete()
        Light.query.filter(Light.id == id).delete()
        db.session.commit()
        totaldingdan(data.oder_id)
        return '200'
    elif request.method == 'POST':
        Light.edit(id)
        data = Light.query.get(id)
        totaldingdan(data.oder_id)
        return '200'


def lighttotal(id):
    data = Light.query.get(id)
    slight = 0
    for i in data.cailiaos:
        if i.cshenhe == '已通过':
            slight = slight + i.ccost
    data.lcost = float('%.2f' % slight)
    db.session.commit()


def totaldingdan(id):
    data2 = Wonnot.query.get(id)
    s = 0
    s1 = 0
    for i in data2.lights:
        s = s + (i.lcount * i.lprice)
        s1 = s1 + i.lcost
    data2.sales = float('%.2f' % s)
    data2.cost = float('%.2f' % s1)
    data2.profit = float('%.2f' % (data2.sales - data2.cost))
    db.session.commit()
