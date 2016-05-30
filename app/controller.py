__author__ = 'Bnizzle'
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from app.models import db, Users, UsersSchema
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

# Init a blueprint
users = Blueprint('users', __name__)

# Init the schema
schema = UsersSchema(strict=True)

# Init the API Object
api = Api(users)


# Create CRUD Classes
class CreateListUsers(Resource):

    def get(self):
        users_query = Users.query.all()
        results = schema.dump(users_query, many=True).data
        return results

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            print(raw_dict)
            user = Users(request_dict['name'], request_dict['email'])
            user.add(user)
            # Shouldn't return password hash
            query = Users.query.get(user.id)
            results = schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class GetUpdateDeleteUser(Resource):
    def get(self, id):
        user_query = Users.query.get_or_404(id)
        result = schema.dump(user_query).data
        return result

    def patch(self, id):
        user = Users.query.get_ir_404(id)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(user, key, value)

            user.update()
            return self.get(id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, id):
        user = Users.query.get_or_404(id)
        try:
            delete = user.delete(user)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

#Map classes to API
api.add_resource(CreateListUsers, '.json')
api.add_resource(GetUpdateDeleteUser, '/&lt;int:id&gt;.json')