from db import db


class CategoryModel(db.Model):
    __tablename__ = 'categorys'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))

    articles = db.relationship('ArticleModel', lazy="dynamic")

    def __init__(self, description):
        self.description = description

    def json(self):
        return {
            'id': self.id,
            'description': self.description,
            'articles': [article.json() for article in self.articles.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
