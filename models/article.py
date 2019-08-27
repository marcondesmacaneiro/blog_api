from db import db

class ArticleModel(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    slug = db.Column(db.String(30))
    description = db.Column(db.String(500))

    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    category = db.relationship('CategoryModel')

    def __init__(self, title, slug, description, category_id):
        self.title = title
        self.slug = slug
        self.description = description
        self.category_id = category_id

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'category_id': self.category_id
        }

