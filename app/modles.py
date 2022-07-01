import json
from flask import request
from app import db


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(64))
    name = db.Column(db.String(64))
    local = db.Column(db.String(64))
    phone = db.Column(db.String(11))
    oders = db.relationship('Wonnot', backref='customer')

    def to_json(self):
        return {
            'id': self.id,
            'companyname': self.company,
            'name': self.name,
            'local': self.local,
            'phone': self.phone
        }

    def edit(id):
        companyname = request.get_json(silent=True)['companyname']
        name = request.get_json(silent=True)['name']
        local = request.get_json(silent=True)['local']
        phone = request.get_json(silent=True)['phone']
        data = Customer.query.get(id)
        for i in data.oders:
            i.name = companyname
        data.company = companyname
        data.name = name
        data.local = local
        data.phone = phone
        db.session.commit()


class Wonnot(db.Model):
    __tablename__ = 'oder'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64))
    number = db.Column(db.String(64))
    name = db.Column(db.String(64))
    phone = db.Column(db.String(11))
    cost = db.Column(db.Float)
    sales = db.Column(db.Float)
    profit = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    lights = db.relationship('Light', backref='oder')

    def to_json(self):
        return {
            'id': self.id,
            'date': self.date,
            'number': self.number,
            'name': self.name,
            'phone': self.phone,
            'cost': self.cost,
            'sales': self.sales,
            'profit': self.profit,
        }

class Light(db.Model):
    __tablename__ = 'light'
    id = db.Column(db.Integer, primary_key=True)
    ltype = db.Column(db.String(32))
    lsort = db.Column(db.String(32))
    lsize = db.Column(db.String(32))
    lcolor = db.Column(db.String(32))
    lcount = db.Column(db.Integer)
    lcost = db.Column(db.Float)
    lprice = db.Column(db.Float)
    image = db.Column(db.String(32))
    oder_id = db.Column(db.Integer, db.ForeignKey('oder.id'))
    cailiaos = db.relationship('Cailiao', backref='light')
    baozhuangs = db.relationship('Baozhuang', backref='light')

    def to_json(self):
        try:
            return {
                'id': self.id,
                'ltype': self.ltype,
                'lsort': self.lsort,
                'lsize': self.lsize,
                'lcolor': self.lcolor,
                'lcount': self.lcount,
                'lcost': self.lcost,
                'lprice': self.lprice,
                'image': json.loads(self.image)
            }
        except:
            return {
                'id': self.id,
                'ltype': self.ltype,
                'lsort': self.lsort,
                'lsize': self.lsize,
                'lcolor': self.lcolor,
                'lcount': self.lcount,
                'lcost': self.lcost,
                'lprice': self.lprice,
            }

    def edit(id):
        data = Light.query.get(id)
        ltype = request.get_json(silent=True)['ltype']
        lsort = request.get_json(silent=True)['lsort']
        lsize = request.get_json(silent=True)['lsize']
        lcolor = request.get_json(silent=True)['lcolor']
        lcount = request.get_json(silent=True)['lcount']
        lprice = request.get_json(silent=True)['lprice']
        data.ltype = ltype
        data.lsort = lsort
        data.lsize = lsize
        data.lcolor = lcolor
        data.lcount = lcount
        data.lprice = lprice
        db.session.commit()


class Cailiao(db.Model):
    __tablename__ = 'cailiao'
    id = db.Column(db.Integer, primary_key=True)
    cdate = db.Column(db.String(32))
    ctype = db.Column(db.String(32))
    cxtype = db.Column(db.String(32))
    coder = db.Column(db.String(32))
    csort = db.Column(db.String(32))
    cguige = db.Column(db.String(32))
    ccolor = db.Column(db.String(32))
    csupplier = db.Column(db.String(32))
    cprice = db.Column(db.Float(10))
    ccount = db.Column(db.Integer)
    cdanwei = db.Column(db.String(10))
    cbeizhu = db.Column(db.String(32))
    ccost = db.Column(db.Float(32))
    cshenhe = db.Column(db.String(5))
    cjingshouren = db.Column(db.String(5))
    cshenheren = db.Column(db.String(5))
    cshenhetime = db.Column(db.String(5))
    light_id = db.Column(db.Integer, db.ForeignKey('light.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self):
        return {
            'id': self.id,
            'cdate': self.cdate,
            'ctype': self.ctype,
            'cxtype': self.cxtype,
            'coder': self.coder,
            'csort': self.csort,
            'cguige': self.cguige,
            'ccolor': self.ccolor,
            'cprice': self.cprice,
            'ccount': self.ccount,
            'cdanwei': self.cdanwei,
            'cbeizhu': self.cbeizhu,
            'ccost': self.ccost,
            'cshenhe': self.cshenhe,
            'csupplier': self.csupplier,
            'cjingshouren': self.cjingshouren,
            'cshenheren': self.cshenheren,
            'cshenhetime': self.cshenhetime
        }


class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(32))
    name = db.Column(db.String(32))
    local = db.Column(db.String(32))
    sort = db.Column(db.String(32))
    phone = db.Column(db.Integer)
    cailiaos = db.relationship('Cailiao', backref='supplier')

    def to_json(self):
        return {
            'id': self.id,
            'company': self.company,
            'name': self.name,
            'local': self.local,
            'phone': self.phone,
            'sort': self.sort
        }


class Type(db.Model):
    __tablename__ = "type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    xTypes = db.relationship('xType', backref='type')

    @staticmethod
    def chushihua():
        db.session.query(Type).delete()
        s = ['原材料', '加工', '表面处理', '电器', '包材', '灯罩', '成品灯', '半成品', '其他']
        for i in s:
            data = Type(name=i)
            db.session.add(data)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


class xType(db.Model):
    __tablename__ = 'xtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @staticmethod
    def chushihua():
        db.session.query(xType).delete()
        s1 = ['铁', '201不锈钢', '304不锈钢', '铝', '铜', '镀锌']
        s2 = ['车加工', '线割', '激光', '焊接']
        s3 = ['抛光', '电镀', '喷漆', 'PVD', '喷粉', '染色', '氧化']
        s4 = ['电源线', '光源', '驱动', '开关', '插座', 'USB', '灯头']
        s5 = ['泡沫', '纸箱', '夹板箱', '托板', '复合棉']
        s6 = ['布罩', '玻璃', '亚克力', '五金罩', '云石', '大理石']
        s7 = ['配件', '标贴', '装柜费', '运费', '易耗品', '工具']
        for i in s1:
            data = xType(name=i, type_id=1)
            db.session.add(data)
        for i in s2:
            data = xType(name=i, type_id=2)
            db.session.add(data)
        for i in s3:
            data = xType(name=i, type_id=3)
            db.session.add(data)
        for i in s4:
            data = xType(name=i, type_id=4)
            db.session.add(data)
        for i in s5:
            data = xType(name=i, type_id=5)
            db.session.add(data)
        for i in s6:
            data = xType(name=i, type_id=6)
            db.session.add(data)
        for i in s7:
            data = xType(name=i, type_id=9)
            db.session.add(data)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(12), nullable=True, unique=True)
    password = db.Column(db.String(12))
    role = db.Column(db.String(12))
    name = db.Column(db.String(12))
    cailiaos = db.relationship('Cailiao', backref='user')

    def to_json(self):
        return {
            'id': self.id,
            'user': self.user,
            'role': self.role,
            'name': self.name,
        }

    @staticmethod
    def chushihua():
        db.session.query(User).delete()
        user = 'admin'
        password = '202cb962ac59075b964b07152d234b70'
        role = '管理员'
        name = '胡际娥'
        data = User(user=user, password=password, role=role, name=name)
        db.session.add(data)
        db.session.commit()


class Baozhuang(db.Model):
    __tablename__ = 'baozhuang'
    id = db.Column(db.Integer, primary_key=True)
    bujian = db.Column(db.String(32))
    jianxiang = db.Column(db.Integer)
    totalnumber = db.Column(db.Integer)
    jweight = db.Column(db.Float(32))
    totaljweight = db.Column(db.Float(32))
    mweight = db.Column(db.Float(32))
    totalmweight = db.Column(db.Float(32))
    long = db.Column(db.Float(32))
    width = db.Column(db.Float(32))
    height = db.Column(db.Float(32))
    volume = db.Column(db.Float(32))
    totalvolume = db.Column(db.Float(32))
    beizhu = db.Column(db.String(32))
    light_id = db.Column(db.Integer, db.ForeignKey('light.id'))

    def to_json(self):
        return {
            'id': self.id,
            'bujian': self.bujian,
            'jianxiang': self.jianxiang,
            'totalnumber': self.totalnumber,
            'jweight': self.jweight,
            'totaljweight': self.totaljweight,
            'mweight': self.mweight,
            'totalmweight': self.totalmweight,
            'long': self.long,
            'width': self.width,
            'height': self.height,
            'volume': self.volume,
            'totalvolume': self.totalvolume,
            'beizhu': self.beizhu,
        }


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(12))

    @staticmethod
    def chushihua():
        db.session.query(Role).delete()
        s = ['管理员', '录单员', '仓管员', '审批员']
        for i in s:
            role = i
            data = Role(role=role)
            db.session.add(data)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'role': self.role,
        }

if __name__ == '__main__':
    db.create_all()
