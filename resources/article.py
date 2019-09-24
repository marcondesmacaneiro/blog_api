from flask_jwt_extended import jwt_refresh_token_required, jwt_required
from flask_restful import Resource, reqparse
from models.article import ArticleModel


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s


class Article(Resource):
    @jwt_required
    def get(self):
        _article_parser = reqparse.RequestParser()
        _article_parser.add_argument('id',
                                     type=non_empty_string,
                                     required=True,
                                     help="The title field is required!"
                                     )
        data = _article_parser.parse_args()
        article = ArticleModel.find_by_id(data['id'])
        if article:
            return article.json()
        return {'message': 'Article not found'}, 404

    @jwt_refresh_token_required
    def post(self):
        _article_parser = reqparse.RequestParser(bundle_errors=True)
        _article_parser.add_argument('title',
                                     type=non_empty_string,
                                     required=True,
                                     help="The title field is required!"
                                     )
        _article_parser.add_argument('slug',
                                     type=non_empty_string,
                                     required=True,
                                     help="The slug field is required!"
                                     )
        _article_parser.add_argument('description',
                                     type=non_empty_string,
                                     required=True,
                                     help="The description field is required!"
                                     )
        _article_parser.add_argument('category_id',
                                     type=non_empty_string,
                                     required=True,
                                     help="The category field is required!"
                                     )
        data = _article_parser.parse_args()
        if ArticleModel.find_by_title(data['title']):
            return {'message': "A article with name {} already exists".format(data['title'])}, 400

        article = ArticleModel(**data)
        try:
            article.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred while creating the article.'}, 500

        return article.json(), 201

    @jwt_refresh_token_required
    def delete(self):
        _article_parser = reqparse.RequestParser(bundle_errors=True)
        _article_parser.add_argument('id',
                                     type=non_empty_string,
                                     required=True,
                                     help="The id field is required!"
                                     )
        data = _article_parser.parse_args()
        article = ArticleModel.find_by_id(data['id'])
        if article:
            article.delete_from_db()
        return {'message': 'Article Deleted'}


class UpdateArticle(Resource):
    @jwt_refresh_token_required
    def put(self, article_id):
        _article_parser = reqparse.RequestParser(bundle_errors=True)

        _article_parser.add_argument('title',
                                     type=non_empty_string,
                                     required=False,
                                     help="The title field is required!"
                                     )
        _article_parser.add_argument('slug',
                                     type=non_empty_string,
                                     required=False,
                                     help="The slug field is required!"
                                     )
        _article_parser.add_argument('description',
                                     type=non_empty_string,
                                     required=False,
                                     help="The description field is required!"
                                     )
        _article_parser.add_argument('category_id',
                                     type=non_empty_string,
                                     required=False,
                                     help="The category field is required!"
                                     )
        data = _article_parser.parse_args()
        article = ArticleModel.find_by_id(article_id)

        if article is None:
            article = ArticleModel(**data)
        else:
            article.title = data['title'] if data['title'] is not None else article.title
            article.slug = data['slug'] if data['slug'] is not None else article.slug
            article.description = data['description'] if data['description'] is not None else article.description
            article.category_id = data['category_id'] if data['category_id'] is not None else article.category_id

        try:
            article.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred while creating the article.'}, 500

        return article.json(), 201


class ArticleList(Resource):
    @jwt_required
    def get(self):
        return {'articles': [x.json() for x in ArticleModel.find_all()]}
