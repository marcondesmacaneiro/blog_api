from db import db


class ArticleModel(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    slug = db.Column(db.String(30))
    image_url = db.Column(db.String(500))
    description = db.Column(db.String(500))

    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    category = db.relationship('CategoryModel')

    def __init__(self, title, slug, image_url, description, category_id):
        self.title = title
        self.slug = slug
        self.image_url = image_url
        self.description = description
        self.category_id = category_id

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'image_url': self.image_url,
            'description': self.description,
            'category_id': self.category_id
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
