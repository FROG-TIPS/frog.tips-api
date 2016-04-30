import os
import base64

from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.sql.functions import random

from frog import db


class Tip(db.Model):
    __tablename__ = 'tips'
    number = db.Column('id', db.Integer, primary_key=True)
    tip = db.Column(db.String(255))
    approved = db.Column(db.Boolean())


class Auth(db.Model):
    __tablename__ = 'auth'
    phrase = db.Column(db.String(256), primary_key=True)
    revoked = db.Column(db.Boolean())


def open_sesame(master_phrase, phrase):
    if phrase == master_phrase:
        return True
    #
    # db.session.query(Auth.phrase, Auth.revoked).filter()
    return db.session.query(Auth.phrase, Auth.revoked) \
                     .filter(Auth.revoked == False) \
                     .filter(Auth.phrase == phrase)\
                     .one_or_none() is not None


def genie_remember_this_phrase():
    random_bytes = os.urandom(32)
    phrase = base64.b64encode(random_bytes).decode('utf-8')
    db.session.add(Auth(phrase=phrase, revoked=False))
    db.session.commit()
    return phrase


def genie_forget_this_phrase(phrase):
    db.session.query(Auth.phrase).filter(Auth.phrase == phrase) \
                                 .update({'revoked': True})
    db.session.commit()


def some_tips_please_sir():
    results = db.session.query(Tip.number, Tip.tip) \
                        .filter(Tip.approved == True) \
                        .order_by(random()).limit(50) \
                        .all()
    return [result._asdict() for result in results]


def just_a_tip_oof_right_there(num):
    result = db.session.query(Tip.number, Tip.tip) \
                       .filter(Tip.approved == True) \
                       .filter(Tip.number == num) \
                       .one_or_none()
    if result is not None:
        return result._asdict()


def the_search_for_spock(fat_blob):
    fat_blob = fat_blob.replace(' ', '%')
    results = db.session.query(Tip.number, Tip.tip) \
                       .filter(Tip.tip.like('%{0}%'.format(fat_blob), escape='\\')) \
                       .limit(10) \
                       .all()
    return [result._asdict() for result in results]
