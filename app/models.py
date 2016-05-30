__author__ = 'Bnizzle'
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class UsersSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=not_blank)
    email = fields.Email()

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}
            # The below type object is a resource identifier object

    class Meta:
        type = 'users'