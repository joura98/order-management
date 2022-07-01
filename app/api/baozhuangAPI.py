from flask import request, jsonify
from app import db
from app.api.auth_token import auth
from app.modles import Baozhuang, Light
from app.api import api


@api.route('/api/baozhuang/<int:id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
@auth.login_required()
def baozhuang(id):
    if request.method == 'GET':
        res = Light.query.get(id)
        list = []
        for i in res.baozhuangs:
            i.long = str(i.long) + '*' + str(i.width) + '*' + str(i.height)
            list.append(i.to_json())
        return jsonify(list)
    if request.method == 'POST':
        bujian = request.get_json(silent=True)['bujian']
        jianxiang = request.get_json(silent=True)['jianxiang']
        totalnumber = int(request.get_json(silent=True)['totalnumber'])
        jweight = float(request.get_json(silent=True)['jweight'])
        mweight = float(request.get_json(silent=True)['mweight'])
        long = float(request.get_json(silent=True)['long'])
        width = float(request.get_json(silent=True)['width'])
        height = float(request.get_json(silent=True)['height'])
        beizhu = request.get_json(silent=True)['beizhu']
        light_id = id
        totaljweight = float('%.2f' % (jweight * totalnumber))
        totalmweight = float('%.2f' % (mweight * totalnumber))
        volume = float('%.2f' % (long * width * height / 1000000))
        totalvolume = float('%.2f' % (volume * totalnumber))
        data = Baozhuang(bujian=bujian, jianxiang=jianxiang, totalnumber=totalnumber, jweight=jweight, mweight=mweight,
                         long=long,
                         width=width, height=height, light_id=light_id, beizhu=beizhu, totaljweight=totaljweight,
                         totalmweight=totalmweight
                         , volume=volume, totalvolume=totalvolume)
        db.session.add(data)
        db.session.commit()
        return jsonify({'code': 200})
    if request.method == 'DELETE':
        Baozhuang.query.filter(Baozhuang.id == id).delete()
        db.session.commit()
        return jsonify({'code': 200})
    if request.method == 'PUT':
        bujian = request.get_json(silent=True)['bujian']
        jianxiang = request.get_json(silent=True)['jianxiang']
        totalnumber = int(request.get_json(silent=True)['totalnumber'])
        jweight = float(request.get_json(silent=True)['jweight'])
        mweight = float(request.get_json(silent=True)['mweight'])
        long = float(request.get_json(silent=True)['long'])
        width = float(request.get_json(silent=True)['width'])
        height = float(request.get_json(silent=True)['height'])
        beizhu = request.get_json(silent=True)['beizhu']
        data = Baozhuang.query.filter(Baozhuang.id == id).first()
        data.bujian = bujian
        data.jianxiang = jianxiang
        data.totalnumber = totalnumber
        data.jweight = jweight
        data.mweight = mweight
        data.long = long
        data.width = width
        data.height = height
        data.beizhu = beizhu
        data.totaljweight = float('%.2f' % (jweight * totalnumber))
        data.totalmweight = float('%.2f' % (mweight * totalnumber))
        volume = float('%.2f' % (long * width * height / 1000000))
        data.volume = volume
        data.totalvolume = float('%.2f' % (volume * totalnumber))
        db.session.commit()
        return jsonify({'code': 200})
