from sqlalchemy import and_
from .extension import db
from passlib.hash import pbkdf2_sha256 as sha256
import pandas as pd
import numpy as np

class UserModel(db.Model):
    __tablename__ = 'users'

    userId = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    userRole = db.Column(db.String(120), nullable=False)
    Email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, userName):
        return cls.query.filter_by(userName=userName).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'userName': x.userName,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete(cls, rowId):
        user = cls.query.filter_by(userId=rowId).first()
        db.session.delete(user)
        db.session.commit()
        return {'message': 'ok'}

    @classmethod
    def deletes(cls, rowId, power):
        user = cls.query.filter_by(userId=rowId).first()
        if power != user.userRole:  # 判断如果权限和自己权限相同则无法进行修改
            db.session.delete(user)
            db.session.commit()
            return {'message': 'ok'}
        else:
            return {'message': 'wrong'}

    @classmethod
    def change_to_db(cls, userId, userRole):
        data = cls.query.get(userId)
        data.userRole = userRole
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def return_alluser(cls, power, allMember):
        def to_json(x):
            return {
                'userId': x.userId,
                'userName': x.userName,
                'userRole': x.userRole,
                'phone': x.phone,
                'Email': x.Email,
            }

        if power == 'super':
            if allMember == 'true':
                return list(map(lambda x: to_json(x), UserModel.query.all()))
            else:
                return list(map(lambda x: to_json(x), cls.query.filter(UserModel.userRole != 'user')))
        elif power == 'admin':
            if allMember == 'true':
                return list(map(lambda x: to_json(x), cls.query.filter(UserModel.userRole != 'super')))
            else:
                return list(map(lambda x: to_json(x), cls.query.filter_by(userRole='admin')))


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class DataModel(db.Model):
    __tablename__ = 'data'

    data_id = db.Column(db.Integer, primary_key=True, nullable=False)
    userName = db.Column(db.String(255), nullable=False)
    beer_name = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    brewery_name = db.Column(db.String(255), nullable=True)
    brewery_id = db.Column(db.String(255), nullable=True)
    abv = db.Column(db.String(255), nullable=True)
    ounces = db.Column(db.String(255), nullable=True)
    style = db.Column(db.String(255), nullable=True)
    id = db.Column(db.String(255), nullable=True)
    index = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def find(cls,index):
        data=cls.query.filter_by(index=index).first()
        return data
    @classmethod
    def Delete(cls, username):
        db.session.query(cls).filter(DataModel.userName == username).delete()
        db.session.commit()

    @classmethod
    def return_allData(cls, username):
        def to_json(x):
            return {
                'index': x.index,
                'id': x.id,
                'beer_name': x.beer_name,
                'style': x.style,
                'ounces': x.ounces,
                'abv': x.abv,
                'brewery_id': x.brewery_id,
                'brewery_name': x.brewery_name,
                'city': x.city,
                'state': x.state,
            }
        return list(map(lambda x: to_json(x), cls.query.filter_by(userName=username)))

    @classmethod
    def changeData(cls, data_, userName):
        user = cls.query.filter(
            and_(DataModel.index == eval(data_.data)['index'],
                 DataModel.userName == userName)).first()  # 组合查询，查询到index和username
        user.index = eval(data_.data)['index']
        user.id = eval(data_.data)['id']
        user.beer_name = eval(data_.data)['beer_name']
        user.style = eval(data_.data)['style']
        user.ounces = eval(data_.data)['ounces']
        user.abv = eval(data_.data)['abv']
        user.brewery_id = eval(data_.data)['brewery_id']
        user.brewery_name = eval(data_.data)['brewery_name']
        user.city = eval(data_.data)['city']
        user.state = eval(data_.data)['state']
        db.session.commit()

    @classmethod
    def delete(cls, index,userName):
        data = cls.query.filter(
            and_(DataModel.index == index,
                 DataModel.userName == userName)).first()
        db.session.delete(data)
        db.session.commit()
        return {'message': 'ok'}

    @classmethod
    def deletes(cls, userName, index):
        data = cls.query.filter(and_(DataModel.index==index,DataModel.userName==userName)).first()
        db.session.delete(data)
        db.session.commit()
        return {'message': 'ok'}

    def to_json(self):
        return {
            'index': self.index,
            'id': self.id,
            'beer_name': self.beer_name,
            'style': self.style,
            'ounces': self.ounces,
            'abv': self.abv,
            'brewery_id': self.brewery_id,
            'brewery_name': self.brewery_name,
            'city': self.city,
            'state': self.state,
        }

    @classmethod
    def ormmodel_todf(cls,userName):
        records = cls.query.filter_by(userName=userName).all()
        df = []
        for record in records:
            df.append(record.to_json())
        df = pd.DataFrame(df)
        return df

    @classmethod
    def detectNull(cls,df):
        df = df.replace('', np.NaN)  # 将表中缺失值替换为NaN的形式
        ex_df = df.loc[df.isnull().any(axis=1)]  # 将表中含有NaN值筛选出
        return ex_df

    @classmethod
    def detectFormat(cls,df):
        df = df.replace('', np.NaN)
        ex_df = df.dropna(subset=['abv'])  # 将abv列为空的行删除
        fina_df = ex_df[ex_df['abv'].str.contains('%')]  # 寻找abv列中元素含有%元组
        return fina_df
    @classmethod
    def datamodel_todict(cls,user):
        index = getattr(user,'index')
        id = getattr(user,'id')
        beer_name = getattr(user,'beer_name')
        style = getattr(user,'style')
        ounces = getattr(user,'ounces')
        abv = getattr(user,'abv')
        brewery_id = getattr(user,'brewery_id')
        brewery_name = getattr(user,'brewery_name')
        city = getattr(user,'city')
        state = getattr(user,'state')
        combine_dict = {
            'index': index,
            'id': id,
            'beer_name': beer_name,
            'style': style,
            'ounces': ounces,
            'abv': abv,
            'brewery_id': brewery_id,
            'brewery_name': brewery_name,
            'city': city,
            'state': state
        }
        return combine_dict
    @classmethod
    def df_tojosn(cls,df):
        datalist=[]
        for i in range(0, len(df)):
            list = df.iloc[i]
            index = list['index']
            id = list['id']
            beer_name = list['beer_name']
            style = list['style']
            ounces = list['ounces']
            abv = list['abv']
            brewery_id = list['brewery_id']
            brewery_name = list['brewery_name']
            city = list['city']
            state = list['state']
            combine_dict1 = {
                'index': index,
                'id': id,
                'beer_name': beer_name,
                'style': style,
                'ounces': ounces,
                'abv': abv,
                'brewery_id': brewery_id,
                'brewery_name': brewery_name,
                'city': city,
                'state': state
            }
            datalist.append(combine_dict1)
        return datalist