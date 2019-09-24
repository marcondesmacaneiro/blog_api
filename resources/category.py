from flask_jwt_extended import jwt_refresh_token_required, jwt_required
from flask_restful import Resource, reqparse
from models.category import CategoryModel


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s


class Category(Resource):
    @jwt_required
    def get(self):
        _category_parser = reqparse.RequestParser()
        _category_parser.add_argument('id',
                                      type=non_empty_string,
                                      required=True,
                                      help="The id field is required!"
                                      )
        data = _category_parser.parse_args()
        category = CategoryModel.find_by_id(data['id'])
        if category:
            return category.json()
        return {'message': 'Category not found'}, 404

    @jwt_refresh_token_required
    def post(self):
        _category_parser = reqparse.RequestParser(bundle_errors=True)
        _category_parser.add_argument('name',
                                      type=non_empty_string,
                                      required=True,
                                      help="The name field is required!"
                                      )
        data = _category_parser.parse_args()
        if CategoryModel.find_by_name(data['name']):
            return {'message': "A category with name {} already exists".format(data['name'])}, 400

        article = CategoryModel(**data)
        try:
            article.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred while creating the category.'}, 500

        return article.json(), 201

    @jwt_refresh_token_required
    def delete(self):
        _category_parser = reqparse.RequestParser(bundle_errors=True)
        _category_parser.add_argument('id',
                                      type=non_empty_string,
                                      required=True,
                                      help="The id field is required!"
                                      )
        data = _category_parser.parse_args()
        category = CategoryModel.find_by_id(data['id'])
        if category:
            category.delete_from_db()
        return {'message': 'Category Deleted'}


class UpdateCategory(Resource):
    @jwt_refresh_token_required
    def put(self, category_id):
        _category_parser = reqparse.RequestParser(bundle_errors=True)
        _category_parser.add_argument('name',
                                      type=non_empty_string,
                                      required=False,
                                      help="The name field is required!"
                                      )
        data = _category_parser.parse_args()
        category = CategoryModel.find_by_id(category_id)

        if category is None:
            category = CategoryModel(**data)
        else:
            category.name = data['name'] if data['name'] is not None else category.name

        try:
            category.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred while creating the category.'}, 500

        return category.json(), 201


class CategoryList(Resource):
    @jwt_required
    def get(self):
        return {'categorys': [x.json() for x in CategoryModel.find_all()]}
