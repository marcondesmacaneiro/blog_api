from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity, jwt_required, get_raw_jwt, get_jti)
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from redis_server import revoked_store, ACCESS_EXPIRES, REFRESH_EXPIRES


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s


class UserRegister(Resource):
    def post(self):
        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument('name',
                                  type=non_empty_string,
                                  required=True,
                                  help="This field cannot be left blank!"
                                  )
        _user_parser.add_argument('email',
                                  type=non_empty_string,
                                  required=True,
                                  help="This field cannot be left blank!"
                                  )
        _user_parser.add_argument('password',
                                  type=non_empty_string,
                                  required=True,
                                  help="This field cannot be left blank!"
                                  )
        data = _user_parser.parse_args()

        if UserModel.find_by_name(data['name']):
            return {"message": "User with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created succesfully"}, 201


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        _user_parser = reqparse.RequestParser(bundle_errors=True)
        _user_parser.add_argument('email',
                                  type=non_empty_string,
                                  required=True,
                                  help="The email field is required!"
                                  )
        _user_parser.add_argument('password',
                                  type=non_empty_string,
                                  required=True,
                                  help="The password field is required!"
                                  )
        data = _user_parser.parse_args()
        user = UserModel.find_by_email(data['email'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
            revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                       'user': user.username()
                   }, 200
        return {'message': 'Invalid Credential'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true', ACCESS_EXPIRES * 1.2)
        return {'message': 'Succesfully logged out.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        access_jti = get_jti(encoded_token=new_token)
        revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        return {'access_token': new_token}, 200
