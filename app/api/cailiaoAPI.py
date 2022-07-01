import time
from flask import request, jsonify
from app import db
from app.api import api
from app.api.auth_token import auth
from app.api.lightAPI import totaldingdan, lighttotal
from app.modles import User, Supplier, Cailiao, Light, Type, Wonnot


@api.route('/api/config', methods=['GET', 'POST'])
@auth.login_required
def config():
    if request.method == 'GET':
        list = []
        cus = db.session.query(User.name, User.id).filter(User.role == '录单员')
        for i in cus:
            list.append({'name': i.name, 'id': i.id})
        return jsonify(list)


@api.route('/api/cailiao', methods=['POST', 'GET'])
@auth.login_required
def getcailiao():
    if request.method == 'POST':
        cdate = request.get_json(silent=True)['cdate']
        cdate = time.localtime(cdate / 1000)
        cdate = time.strftime('%Y-%m-%d', cdate)
        ctype = request.get_json(silent=True)['ctype']
        cxtype = request.get_json(silent=True)['cxtype']
        coder = request.get_json(silent=True)['coder']
        csupplier = request.get_json(silent=True)['csupplier']
        csort = request.get_json(silent=True)['csort']
        cguige = request.get_json(silent=True)['cguige']
        ccolor = request.get_json(silent=True)['ccolor']
        ccount = request.get_json(silent=True)['ccount']
        cdanwei = request.get_json(silent=True)['cdanwei']
        cprice = request.get_json(silent=True)['cprice']
        cbeizhu = request.get_json(silent=True)['cbeizhu']
        light_id = int(request.get_json(silent=True)['light_id'])
        rudanname = request.get_json(silent=True)['rudanname']
        s = User.query.filter(rudanname == User.name)
        for i in s:
            user_id = i.id
        ccost = float('%.2f' % (float(cprice) * float(ccount)))
        cshenhe = '未审核'
        light_id = light_id
        cjingshouren = rudanname
        data1 = Supplier.query.filter(Supplier.company == csupplier)
        for i in data1:
            supplier_id = i.id
        data = Type.query.get(ctype)
        ctype = data.name
        data = Cailiao(cdate=cdate, ctype=ctype, cxtype=cxtype, coder=coder, csort=csort, cguige=cguige, ccolor=ccolor,
                       cprice=cprice, ccount=ccount, cdanwei=cdanwei, cbeizhu=cbeizhu, ccost=ccost, cshenhe=cshenhe,
                       light_id=light_id, csupplier=csupplier, supplier_id=supplier_id, user_id=user_id,
                       cjingshouren=cjingshouren)
        db.session.add(data)
        db.session.commit()
        return '200'
    if request.method == 'GET':
        data = Cailiao.query.all()
        for i in data:
            list.append(i.to_json())
        return jsonify(list)


@api.route('/api/cailiao/<int:id>', methods=['POST', 'GET', 'DELETE'])
@auth.login_required
def viewcailiao(id):
    if request.method == 'GET':
        data = Light.query.get(id)
        list = []
        for i in data.cailiaos:
            list.append(i.to_json())
        return jsonify(list)
    if request.method == 'DELETE':
        Cailiao.query.filter(Cailiao.id == id).delete()
        db.session.commit()
        return '200'


@api.route('/api/shenhe/<int:id>', methods=['POST'])
@auth.login_required
def shenhe(id):
    if request.method == 'POST':
        cshenheren = request.get_json(silent=True)['cshenheren']
        data = Cailiao.query.get(id)
        data.cshenhe = '已通过'
        data.cshenhetime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        data.cshenheren = cshenheren
        db.session.commit()
        lightid = data.light_id
        data2 = Light.query.get(lightid)
        number = data2.oder_id
        lighttotal(lightid)
        totaldingdan(number)
        return '200'


@api.route('/api/viewcailiao', methods=['GET', 'POST'])
@auth.login_required
def viecailiao():
    if request.method == 'GET':
        list = []
        data = Type.query.all()
        for i in data:
            list.append(i.to_json())
        return jsonify(list)
    if request.method == 'POST':
        list = []
        data = Supplier.query.all()
        for i in data:
            list.append(i.to_json())
        return jsonify(list)


@api.route('/api/viewcailiao/<int:id>', methods=['GET'])
@auth.login_required
def viecailiao1(id):
    data = Type.query.get(id)
    list = []
    for i in data.xTypes:
        list.append(i.to_json())
    return jsonify(list)


@api.route('/api/editcailiao/<int:id>', methods=['GET', 'POST'])
@auth.login_required
def editcailiao(id):
    if request.method == 'POST':
        ctype = request.get_json(silent=True)['ctype']
        cxtype = request.get_json(silent=True)['cxtype']
        coder = request.get_json(silent=True)['coder']
        csupplier = request.get_json(silent=True)['csupplier']
        csort = request.get_json(silent=True)['csort']
        cguige = request.get_json(silent=True)['cguige']
        ccolor = request.get_json(silent=True)['ccolor']
        ccount = request.get_json(silent=True)['ccount']
        cdanwei = request.get_json(silent=True)['cdanwei']
        cprice = request.get_json(silent=True)['cprice']
        cbeizhu = request.get_json(silent=True)['cbeizhu']
        data = Cailiao.query.get(id)
        s = Type.query.get(ctype)
        data.ctype = s.name
        data.cxtype = cxtype
        data.coder = coder
        data.csupplier = csupplier
        data.csort = csort
        data.cguige = cguige
        data.ccolor = ccolor
        data.ccount = ccount
        data.cdanwei = cdanwei
        data.cprice = cprice
        data.cbeizhu = cbeizhu
        supplier_id = Supplier.query.filter(Supplier.company == csupplier).first().id
        data.supplier_id = supplier_id
        data.ccost = float('%.2f' % (float(cprice) * float(ccount)))
        db.session.commit()
        return '200'


@api.route('/api/sviewcailiao/<int:id>', methods=['GET', 'POST'])
@auth.login_required
def sviewcailiao(id):
    if request.method == 'GET':
        data = Supplier.query.get(id)
        list = []
        for i in data.cailiaos:
            data2 = Light.query.get(i.light_id)
            data3 = Wonnot.query.get(data2.oder_id)
            A = ({'number': data3.number, 'ltype': data2.ltype})
            A.update(i.to_json())
            list.append(A)
        return jsonify(list)
    if request.method == 'POST':
        data = Supplier.query.get(id)
        ctime = request.get_json(silent=True)['time']
        time1 = ctime[0] / 1000
        time2 = ctime[1] / 1000
        list = []
        for i in data.cailiaos:
            s = int(time.mktime(time.strptime(i.cdate, "%Y-%m-%d")))
            if time1 < s < time2:
                data2 = Light.query.get(i.light_id)
                data3 = Wonnot.query.get(data2.oder_id)
                A = ({'number': data3.number, 'ltype': data2.ltype})
                A.update(i.to_json())
                list.append(A)
        return jsonify(list)


@api.route('/api/mingxiacailiao', methods=['POST'])
@auth.login_required
def mingxiacailiao():
    if request.method == 'POST':
        name = request.get_json(silent=True)['name']
        page = request.get_json(silent=True)['page']
        pagesize = request.get_json(silent=True)['pagesize']
        reslist = []
        data = User.query.filter(name == User.name).first()
        totalpage = len(data.cailiaos)
        data2 = data.cailiaos[-(((page - 1) * pagesize) + 1):-(((page) * pagesize) + 1):-1]
        for i in data2:
            light = Light.query.get(i.light_id)
            oder = Wonnot.query.get(light.oder_id)
            A = {'number': oder.number, 'ltype': light.ltype}
            A.update(i.to_json())
            reslist.append(A)
        reslist.append({'totalpage': totalpage})
        return jsonify(reslist)


@api.route('/api/mingxiacailiao/<int:id>', methods=['POST'])
@auth.login_required
def mingxiacailiao2(id):
    if request.method == 'POST':
        if id == 1:
            name = request.get_json(silent=True)['name']
            data = User.query.filter(User.name == name).first()
            list = []
            for i in data.cailiaos:
                light = Light.query.get(i.light_id)
                oder = Wonnot.query.get(light.oder_id)
                A = {'ltype': light.ltype, 'number': oder.number}
                A.update(i.to_json())
                list.append(A)
            return jsonify(list)


@api.route('/api/bijia/<int:id>', methods=['POST'])
@auth.login_required()
def bijia(id):
    if request.method == 'POST':
        if id == 1:
            page = request.get_json(silent=True)['page']
            pagesize = request.get_json(silent=True)['pagesize']
            totalpage = Cailiao.query.count()
            data = Cailiao.query.order_by(Cailiao.ctype).paginate(page, pagesize).items
            reslist = []
            for i in data:
                light = Light.query.get(i.light_id)
                order = Wonnot.query.get(light.oder_id)
                A = {'number': order.number, 'ltype': light.ltype}
                A.update(i.to_json())
                reslist.append(A)
            reslist.append({'totalpage': totalpage})
            return jsonify(reslist)
        if id == 2:
            number = request.get_json(silent=True)['ordernumber']
            ltype = request.get_json(silent=True)['ltype']
            xtype = request.get_json(silent=True)['xtype']
            coder = request.get_json(silent=True)['coder']
            csort = request.get_json(silent=True)['csort']
            cguige = request.get_json(silent=True)['cguige']
            csupplier = request.get_json(silent=True)['csupplier']
            if (number + ltype + xtype + coder + csort + cguige + csupplier):
                data = Cailiao.query.all()
                list = []
                for i in data:
                    light = Light.query.get(i.light_id)
                    oder = Wonnot.query.get(light.oder_id)
                    A = {'number': oder.number, 'ltype': light.ltype}
                    A.update(i.to_json())
                    list.append(A)
                return jsonify(list)
            else:
                return jsonify({'code': 500})
