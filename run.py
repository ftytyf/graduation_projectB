from flask import Flask
from flask_restful import Api
from resourcesmodule import resources
from modelmodule.extension import db
from modelmodule import models
from flask_jwt_extended import JWTManager
import errors

app = Flask(__name__)
api = Api(app, errors=errors.error)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.getAllUserList, '/getAllUserList')
api.add_resource(resources.SecretResource, '/secret')
api.add_resource(resources.GetuserInfo, '/getUserInfo')
api.add_resource(resources.getUserRoutes, '/getUserRoutes')
api.add_resource(resources.updateToken,'/updateToken')
api.add_resource(resources.Uploaddirty,'/Uploaddirty')
api.add_resource(resources.getData,'/getDataList')
api.add_resource(resources.userDel,'/userDel')
api.add_resource(resources.userDels,'/userDels')
api.add_resource(resources.userRoleChange,'/userRoleChange')
api.add_resource(resources.dataChange,'/dataChange')
api.add_resource(resources.dataDel,'/dataDel')
api.add_resource(resources.dataDels,'/dataDels')
api.add_resource(resources.nullPresent,'/nullPresent')
api.add_resource(resources.formatPresent,'/formatPresent')
api.add_resource(resources.faultPresent,'/faultPresent')
api.add_resource(resources.Uploadrule,'/Uploadrule')
api.add_resource(resources.stateCandidate,'/stateCandidate')
api.add_resource(resources.abvCandidate,'/abvCandidate')
api.add_resource(resources.cityCandidate,'/cityCandidate')
api.add_resource(resources.handrepair,'/handrepair')
api.add_resource(resources.autorepair,'/autorepair')
api.add_resource(resources.download,'/download')
api.add_resource(resources.faulttype,'/faulttype')
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "fan6688."
DATABASE = "database_learn"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset" \
                                        f"=utf8mb4"
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

if __name__ == '__main__':
    app.run(debug=True)

