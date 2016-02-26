from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.sql.functions import random

from frog import db


class Tip(db.Model):
    __tablename__ = 'tips'
    number = db.Column('id', db.Integer, primary_key=True)
    tip = db.Column(db.String(255))
    approved = db.Column(db.Boolean())


def some_tips_please_sir():
    results = db.session.query(Tip.number, Tip.tip).filter(Tip.approved == True).order_by(random()).limit(50).all()
    return [result._asdict() for result in results]


def just_a_tip_oof_right_there(num):
    result = db.session.query(Tip.number, Tip.tip).filter(Tip.approved == True).filter(Tip.number == num).one_or_none()
    if result is not None:
        return result._asdict()
