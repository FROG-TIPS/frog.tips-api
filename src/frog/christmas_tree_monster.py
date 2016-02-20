from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.sql.functions import random

from frog import db


class Tip(db.Model):
    __tablename__ = 'tips'
    number = db.Column('id', db.Integer, primary_key=True)
    tip = db.Column(db.String(255))
    approved = db.Column(db.Boolean())

    def to_dict(self):
        keys = [prop.key for prop in class_mapper(self.__class__).iterate_properties if isinstance(prop, ColumnProperty)]
        return dict([(key, getattr(self, key)) for key in keys])


def some_tips_please_sir():
    return db.session.query(Tip).filter(Tip.approved == True).order_by(random()).limit(50).all()


def just_a_tip_oof_right_there(num):
    return db.session.query(Tip).filter(Tip.approved == True).filter(Tip.number == num).one_or_none()
