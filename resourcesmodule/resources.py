from time import time
import os
import pandas as pd
import numpy as np
from flask import send_file
from flask_restful import Resource, reqparse
from modelmodule.models import UserModel, DataModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt,
                                decode_token)
from modelmodule.models import RevokedTokenModel
from routemodule.routechoose import router
from werkzeug.datastructures import FileStorage
from function_testmodule.values_true import breweryid_city,breweryid_state

parser = reqparse.RequestParser()
parser.add_argument('userName', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)

register_parser = reqparse.RequestParser()
register_parser.add_argument('userName', help='This field cannot be blank', required=True)
register_parser.add_argument('pwd', help='This field cannot be blank', required=True)

tokenParser = reqparse.RequestParser()
parser.add_argument('refresh_token')

member_parser = reqparse.RequestParser()
member_parser.add_argument('power', required=True)
member_parser.add_argument('all', required=True)

parser_file = reqparse.RequestParser()
parser_file.add_argument('file', type=FileStorage, location="files")

parser_file1 = reqparse.RequestParser()
parser_file1.add_argument('file', type=FileStorage, location="files")

rowId_parser = reqparse.RequestParser()
rowId_parser.add_argument('rowId', help='This field cannot be blank', required=True)

parser_dels = reqparse.RequestParser()
parser_dels.add_argument('rowId', action='append', required=True)
parser_dels.add_argument('power', required=True)

parser_role = reqparse.RequestParser()
parser_role.add_argument('userid', required=True)
parser_role.add_argument('userRole', required=True)

parser_dataChange = reqparse.RequestParser()
parser_dataChange.add_argument('data', required=True)
parser_dataChange.add_argument('type', required=True)

parser_dataDel = reqparse.RequestParser()
parser_dataDel.add_argument('index', required=True)

parser_datadels = reqparse.RequestParser()
parser_datadels.add_argument('index', action='append', required=True)

parser_abvCandidate = reqparse.RequestParser()
parser_abvCandidate.add_argument('index', required=True)

parser_stateCandidate = reqparse.RequestParser()
parser_stateCandidate.add_argument('index', required=True)

parser_cityCandidate = reqparse.RequestParser()
parser_cityCandidate.add_argument('index', required=True)

parser_handrepair=reqparse.RequestParser()
parser_handrepair.add_argument('data',required=True)



class UserRegistration(Resource):
    def post(self):
        data = register_parser.parse_args()
        if UserModel.find_by_username(data['userName']):
            return {'message': '用户 {} 已经存在'.format(data['userName'])}

        new_user = UserModel(
            userName=data['userName'],
            password=UserModel.generate_hash(data['pwd']),
            userRole='user'
        )

        new_user.save_to_db()
        data_ = {'code': 200, 'messsage': 'User {} was created'.format(data['userName'])}
        return {
            'code': 200,
            "data": data_
        }


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()  # 接受参数的域
        current_user = UserModel.find_by_username(data['userName'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['userName'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            token = create_access_token(identity=data['userName'])
            refreshToken = create_refresh_token(identity=data['userName'])
            data_ = {'token': token, 'refreshToken': refreshToken}
            return {
                'code': 200,
                'message': 'Logged in as {}'.format(current_user.userName),
                'data': data_
            }
        else:
            return {'message': '密码错误'}


class UserLogoutAccess(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']

        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {'message': 'Access token has been revoked'}


class UserLogoutRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {'token': token}


class getAllUserList(Resource):
    def post(self):
        data = member_parser.parse_args()
        data_member = UserModel.return_alluser(data['power'], data['all'])
        return {
            'code': 200,
            'message': 'ok',
            'data': data_member
        }


class SecretResource(Resource):
    @jwt_required()
    def get(self):
        return {
            'answer': 42
        }


class GetuserInfo(Resource):
    @jwt_required()
    def get(self):
        userName = get_jwt_identity()
        current_user = UserModel.find_by_username(userName)
        userInfo = {'userId': current_user.userId, 'userName': current_user.userName, 'userRole': current_user.userRole}
        return {
            'code': 200,
            'message': 'ok',
            'data': userInfo
        }


class getUserRoutes(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        current_user = UserModel.find_by_username(userName)
        data_ = {'routes': router[current_user.userRole], 'home': 'dashboard_analysis'}
        return {
            'code': 200,
            'message': 'ok',
            'data': data_
        }


class updateToken(Resource):
    def post(self):
        refresh_token = tokenParser.parse_args('refreshToken')
        current_user = decode_token(refresh_token)['sub']
        expire_time = decode_token(refresh_token)['exp']
        if int(time()) <= expire_time:
            token = create_access_token(identity=current_user)
            data = {'token': token, 'refreshToken': refresh_token}
            return {
                'code': 200,
                'message': 'ok',
                'data': data
            }
        else:
            return {
                'code': 3000,
                'message': 'ok',
                'data': None
            }


class Uploaddirty(Resource):
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        data = parser_file.parse_args()
        DataModel.Delete(username)
        file = data['file']
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'files', file.filename)
        file.save(path)
        f = open(path, encoding='gb18030', errors='ignore')
        data_pd = pd.read_csv(f)
        data_pd = data_pd.where(data_pd.notnull(), None)
        for i in range(0, len(data_pd)):
            list = data_pd.iloc[i]
            new_data = DataModel(
                userName=username,
                index=list['index'],
                id=list['id'],
                beer_name=list['beer_name'],
                style=list['style'],
                ounces=list['ounces'],
                abv=list['abv'],
                brewery_id=list['brewery_id'],
                brewery_name=list['brewery_name'],
                city=list['city'],
                state=list['state']
            )
            new_data.save_to_db()
        return {
            'code': 200,
            'message': 'ok',
        }


class Uploadrule(Resource):
    def post(self):
        data = parser_file1.parse_args()
        file = data['file']
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'files', file.filename)
        file.save(path)


class getData(Resource):
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        data = DataModel.return_allData(username)
        return {
            'code': 200,
            'message': 'ok',
            'data': data,
        }


class userDel(Resource):
    def post(self):
        data = rowId_parser.parse_args()
        userId = data['rowId']
        UserModel.delete(userId)
        return {
            'code': 200
        }


class userDels(Resource):
    def post(self):
        data = parser_dels.parse_args()
        for id in data['rowId']:
            UserModel.deletes(id, data['power'])
        return {
            'code': 200,
            'message': 'ok',
        }


class userRoleChange(Resource):
    def post(self):
        data = parser_role.parse_args()
        userId = data["userid"],
        userRole = data["userRole"]
        if userRole == '2':
            userRole = 'admin'
        elif userRole == '3':
            userRole = 'user'
        else:
            userRole = 'super'
        UserModel.change_to_db(userId, userRole)
        backdata = {'code': 200, 'message': '用户身份更改成功'}
        return {
            'code': 200,
            'message': 'ok',
            'data': backdata
        }


class dataChange(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        data_ = parser_dataChange.parse_args()
        if data_.type == 'edit':
            DataModel.changeData(data_, userName)
        else:
            newData = DataModel(
                userName=userName,
                index=eval(data_.data)['index'],
                id=eval(data_.data)['id'],
                beer_name=eval(data_.data)['beer_name'],
                style=eval(data_.data)['style'],
                ounces=eval(data_.data)['ounces'],
                abv=eval(data_.data)['abv'],
                brewery_id=eval(data_.data)['brewery_id'],
                brewery_name=eval(data_.data)['brewery_name'],
                city=eval(data_.data)['city'],
                state=eval(data_.data)['state'],
            )
            newData.save_to_db()
        return {
            'code': 200,
            'message': 'ok'
        }


class dataDel(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        data_ = parser_dataDel.parse_args()
        index = data_['index']
        DataModel.delete(index, userName)
        return {
            'code': 200
        }


class dataDels(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        data = parser_datadels.parse_args()
        for index in data['index']:
            DataModel.deletes(userName, index)
        return {
            'code': 200,
            'message': 'ok',
        }


class nullPresent(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        df = DataModel.ormmodel_todf(userName)
        df = DataModel.detectNull(df)
        data = DataModel.df_tojosn(df)
        return {
            'code': 200,
            'message': 'ok',
            'data': data
        }


class formatPresent(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        df = DataModel.ormmodel_todf(userName)
        df = DataModel.detectFormat(df)
        data = DataModel.df_tojosn(df)
        return {
            'code': 200,
            'message': 'ok',
            'data': data
        }


class faultPresent(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        df = DataModel.ormmodel_todf(userName)
        city_fault = []  # 定义city错误列表
        df = df.replace('', np.NaN)
        for i in range(0, len(df)):
            list1 = df.iloc[i]
            index = list1['index']
            id = list1['id']
            beer_name = list1['beer_name']
            style = list1['style']
            ounces = list1['ounces']
            abv = list1['abv']
            brewery_id = list1['brewery_id']
            brewery_name = list1['brewery_name']
            city = list1['city']
            state = list1['state']
            if breweryid_city.__contains__(str(brewery_id)) and city != breweryid_city[str(brewery_id)]:
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
                city_fault.append(combine_dict1)
        data = city_fault
        return {
            'code': 200,
            'message': 'ok',
            'data': data
        }


class stateCandidate(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        df = DataModel.ormmodel_todf(userName)
        temp = parser_stateCandidate.parse_args()
        list0 = DataModel.find(temp['index'])
        df = df.replace('', np.NaN)  # 将表中缺失值替换为NaN的形式
        df = df.dropna(axis=0, how='any', subset='state')
        jaccardIndex_dict = {}  # 存储杰卡德系数的字典
        union = 16  # 两行属性除去索引和缺失的属性（并集）
        for i in range(0, len(df)):
            intersection = 1
            list1 = df.iloc[i]
            if getattr(list0, 'id') == list1['id']:
                intersection = intersection + 1
            if getattr(list0, 'beer_name') == list1['beer_name']:
                intersection = intersection + 1
            if getattr(list0, 'style') == list1['style']:
                intersection = intersection + 1
            if getattr(list0, 'ounces') == list1['ounces']:
                intersection = intersection + 1
            if getattr(list0, 'abv') == list1['abv']:
                intersection = intersection + 1
            if getattr(list0, 'brewery_id') == list1['brewery_id']:
                intersection = intersection + 1
            if getattr(list0, 'brewery_name') == list1['brewery_name']:
                intersection = intersection + 1
            if getattr(list0, 'city') == list1['city']:
                intersection = intersection + 1
            if getattr(list0, 'index') == list1['index']:
                continue
            else:
                jaccardIndex = intersection / union
            index = list1['index']
            jaccardIndex_dict[str(index)] = jaccardIndex

        maxDistance = 0
        firstIndex = 1
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value:
                maxDistance = value
                firstIndex = key
        jaccardIndex_dict.pop(firstIndex)
        maxDistance = 0
        secondIndex = 1
        firstdata = DataModel.datamodel_todict(DataModel.find(firstIndex))['state']
        if firstIndex == 1:
            secondIndex = 2
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value and DataModel.datamodel_todict(DataModel.find(key))['state'] != firstdata:
                maxDistance = value
                secondIndex = key
        jaccardIndex_dict.pop(secondIndex)
        maxDistance = 0
        thirdIndex = 1
        seconddata = DataModel.datamodel_todict(DataModel.find(secondIndex))['state']
        if secondIndex == 1 or secondIndex == 2:
            thirdIndex = 3
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value and DataModel.datamodel_todict(DataModel.find(firstIndex))['state'] != (
                    firstdata or seconddata):
                maxDistance = value
                thirdIndex = key
        data = []
        first0 = DataModel.find(firstIndex)
        first = DataModel.datamodel_todict(first0)
        data.append(first['state'])
        second0 = DataModel.find(secondIndex)
        second = DataModel.datamodel_todict(second0)
        data.append(second['state'])
        third0 = DataModel.find(thirdIndex)
        third = DataModel.datamodel_todict(third0)
        data.append(third['state'])
        return {
            'code': 200,
            'message': 'ok',
            'data': data
        }


class abvCandidate(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        df = DataModel.ormmodel_todf(userName)
        temp = parser_abvCandidate.parse_args()
        list0 = DataModel.find(temp['index'])
        df = df.replace('', np.NaN)  # 将表中缺失值替换为NaN的形式
        df = df.dropna(axis=0, how='any', subset='abv')

        jaccardIndex_dict = {}  # 存储杰卡德系数的字典
        union = 16  # 两行属性除去索引和缺失的属性（并集）
        for i in range(0, len(df)):
            intersection = 1
            list1 = df.iloc[i]
            if getattr(list0, 'id') == list1['id']:
                intersection = intersection + 1
            if getattr(list0, 'beer_name') == list1['beer_name']:
                intersection = intersection + 1
            if getattr(list0, 'style') == list1['style']:
                intersection = intersection + 1
            if getattr(list0, 'ounces') == list1['ounces']:
                intersection = intersection + 1
            if getattr(list0, 'brewery_id') == list1['brewery_id']:
                intersection = intersection + 1
            if getattr(list0, 'brewery_name') == list1['brewery_name']:
                intersection = intersection + 1
            if getattr(list0, 'city') == list1['city']:
                intersection = intersection + 1
            if getattr(list0, 'state') == list1['state']:
                intersection = intersection + 1
            if getattr(list0, 'index') == list1['index']:
                continue
            else:
                jaccardIndex = intersection / union
            index = list1['index']
            jaccardIndex_dict[str(index)] = jaccardIndex

        maxDistance = 0
        firstIndex = 1
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value:
                maxDistance = value
                firstIndex = key
        jaccardIndex_dict.pop(firstIndex)
        maxDistance = 0
        secondIndex = 1
        firstdata = DataModel.datamodel_todict(DataModel.find(firstIndex))['abv']
        if firstIndex == 1:
            secondIndex = 2
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value and DataModel.datamodel_todict(DataModel.find(key))['abv'] != firstdata:
                maxDistance = value
                secondIndex = key
        jaccardIndex_dict.pop(secondIndex)
        maxDistance = 0
        thirdIndex = 1
        seconddata = DataModel.datamodel_todict(DataModel.find(secondIndex))['abv']
        if secondIndex == 1 or secondIndex == 2:
            thirdIndex = 3
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value and DataModel.datamodel_todict(DataModel.find(firstIndex))['abv'] != (
                    firstdata or seconddata):
                maxDistance = value
                thirdIndex = key
        data = []
        first0 = DataModel.find(firstIndex)
        first = DataModel.datamodel_todict(first0)
        data.append(first['abv'])
        second0 = DataModel.find(secondIndex)
        second = DataModel.datamodel_todict(second0)
        data.append(second['abv'])
        third0 = DataModel.find(thirdIndex)
        third = DataModel.datamodel_todict(third0)
        data.append(third['abv'])
        return {
            'code': 200,
            'message': 'ok',
            'data': data
        }

class cityCandidate(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        df = DataModel.ormmodel_todf(userName)
        temp = parser_cityCandidate.parse_args()
        list0 = DataModel.find(temp['index'])
        df = df.replace('', np.NaN)  # 将表中缺失值替换为NaN的形式
        jaccardIndex_dict = {}  # 存储杰卡德系数的字典
        union = 16  # 两行属性除去索引和缺失的属性（并集）
        for i in range(0, len(df)):
            intersection = 1
            list1 = df.iloc[i]
            if getattr(list0, 'id') == list1['id']:
                intersection = intersection + 1
            if getattr(list0, 'beer_name') == list1['beer_name']:
                intersection = intersection + 1
            if getattr(list0, 'style') == list1['style']:
                intersection = intersection + 1
            if getattr(list0, 'ounces') == list1['ounces']:
                intersection = intersection + 1
            if getattr(list0, 'abv') == list1['abv']:
                intersection = intersection + 1
            if getattr(list0, 'brewery_id') == list1['brewery_id']:
                intersection = intersection + 1
            if getattr(list0, 'brewery_name') == list1['brewery_name']:
                intersection = intersection + 1
            if getattr(list0, 'state') == list1['state']:
                intersection = intersection + 1
            if getattr(list0, 'index') == list1['index']:
                continue
            else:
                jaccardIndex = intersection / union
            index = list1['index']
            jaccardIndex_dict[str(index)] = jaccardIndex

        maxDistance = 0
        firstIndex = 1
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value:
                maxDistance = value
                firstIndex = key
        jaccardIndex_dict.pop(firstIndex)
        maxDistance = 0
        secondIndex = 1
        firstdata = DataModel.datamodel_todict(DataModel.find(firstIndex))['city']
        if firstIndex == 1:
            secondIndex = 2
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value and DataModel.datamodel_todict(DataModel.find(key))['city'] != firstdata:
                maxDistance = value
                secondIndex = key
        jaccardIndex_dict.pop(secondIndex)
        maxDistance = 0
        thirdIndex = 1
        seconddata = DataModel.datamodel_todict(DataModel.find(secondIndex))['city']
        if secondIndex == 1 or secondIndex == 2:
            thirdIndex = 3
        for key, value in jaccardIndex_dict.items():
            if maxDistance < value and DataModel.datamodel_todict(DataModel.find(firstIndex))['city'] != (
                    firstdata or seconddata):
                maxDistance = value
                thirdIndex = key
        data = []
        first0 = DataModel.find(firstIndex)
        first = DataModel.datamodel_todict(first0)
        data.append(first['city'])
        second0 = DataModel.find(secondIndex)
        second = DataModel.datamodel_todict(second0)
        data.append(second['city'])
        third0 = DataModel.find(thirdIndex)
        third = DataModel.datamodel_todict(third0)
        data.append(third['city'])
        return {
            'code': 200,
            'message': 'ok',
            'data': data
        }
class handrepair(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        data_=parser_handrepair.parse_args()
        DataModel.changeData(data_,userName)
        return {
            'code': 200,
            'message': 'ok',
            'data':{
                "userName":userName
            }
        }

class autorepair(Resource):
    @jwt_required()
    def post(self):
        userName=get_jwt_identity()
        df = DataModel.ormmodel_todf(userName)
        df = df.replace('', np.NaN)
        for i in range(0, len(df)):
            abv = str(df.loc[i, 'abv'])
            brewery_id = df.loc[i, 'brewery_id']
            abv = abv.replace('%', '')
            df.loc[i, 'abv'] = abv
            if df.loc[i, 'abv'] == 'nan':
                df.loc[i, 'abv'] = '0.05'
            if breweryid_city.__contains__(str(brewery_id)):
                df.loc[i, 'city'] = breweryid_city.get(str(brewery_id))
            if breweryid_state.__contains__(str(brewery_id)):
                df.loc[i, 'state'] = breweryid_state.get(str(brewery_id))
        DataModel.Delete(userName)
        for j in range(0, len(df)):
            list = df.iloc[j]
            new_data = DataModel(
                userName=userName,
                index=list['index'],
                id=list['id'],
                beer_name=list['beer_name'],
                style=list['style'],
                ounces=list['ounces'],
                abv=list['abv'],
                brewery_id=list['brewery_id'],
                brewery_name=list['brewery_name'],
                city=list['city'],
                state=list['state']
            )
            new_data.save_to_db()
        return {
            'code': 200,
            'message': 'ok'
        }

class download(Resource):
    @jwt_required()
    def post(self):
        userName = get_jwt_identity()
        outpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'files', 'clean.csv')
        df = DataModel.ormmodel_todf(userName)
        df.replace('nan', '', inplace=True)
        df.to_csv(outpath, index=False)
        return send_file(outpath)

class faulttype(Resource):
    @jwt_required()
    def post(self):
        userName=get_jwt_identity()
        df = DataModel.ormmodel_todf(userName)
        df = df.replace('', np.NaN)
        null=len(df.loc[df.isnull().any(axis=1)])
        ex_df = df.dropna(subset=['abv'])  # 将abv列为空的行删除
        format = len(ex_df[ex_df['abv'].str.contains('%')])  # 寻找abv列中元素含有%元组
        city_fault = []  # 定义city错误列表
        for i in range(0, len(df)):
            list1 = df.iloc[i]
            index = list1['index']
            id = list1['id']
            beer_name = list1['beer_name']
            style = list1['style']
            ounces = list1['ounces']
            abv = list1['abv']
            brewery_id = list1['brewery_id']
            brewery_name = list1['brewery_name']
            city = list1['city']
            state = list1['state']
            if breweryid_city.__contains__(str(brewery_id)) and city != breweryid_city[str(brewery_id)]:
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
                city_fault.append(combine_dict1)
        fault=len(city_fault)
        data=[null,format,fault]
        return {
            'code':200,
            'message':'ok',
            'data':data
        }