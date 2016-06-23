import os
import base64
import functools
import datetime

from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.sql.functions import random
from sqlalchemy.exc import OperationalError, IntegrityError
import jsonpatch

from frog import db


class as_dict(object):
    def __init__(self, single=False):
        self.single_item = single

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Allow Nones to fall through
            if result is not None:
                if self.single_item:
                    return result._asdict()
                else:
                    as_list = list(result)
                    return [item._asdict() for item in as_list]

        return wrapper


class Tip(db.Model):
    __tablename__ = 'tips'
    number = db.Column('id', db.Integer, primary_key=True)
    tip = db.Column(db.String(255), nullable=False)
    approved = db.Column(db.Boolean(), nullable=False)
    tweeted = db.Column(db.TIMESTAMP(timezone=True), nullable=True)


class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    revoked = db.Column(db.Boolean())


## DEAL WITH THAT TROUBLESOME GENIE.

class PhraseError(Exception):
    pass


def open_sesame(master_phrase, phrase):
    if phrase == master_phrase:
        return True

    try:
        return db.session.query(Auth.phrase, Auth.revoked) \
                         .filter(Auth.revoked == False) \
                         .filter(Auth.phrase == phrase) \
                         .one_or_none() is not None
    except OperationalError:
        return False


def genie_remember_this_phrase(comment):
    try:
        # OH BOY, OUR OWN CRYPTO!!!
        random_bytes = os.urandom(32)
        phrase = base64.b64encode(random_bytes).decode('utf-8')
        auth = Auth(phrase=phrase, revoked=False, comment=comment)
        db.session.add(auth)
        db.session.commit()
        return auth.phrase, auth.id
    except OperationalError:
        raise PhraseError('PHRASE COULD NOT BE REMEMBERED.')


def genie_forget_this_phrase(id):
    try:
        db.session.query(Auth.id).filter(Auth.id == id) \
                                 .update({'revoked': True})
        db.session.commit()
    except OperationalError:
        raise PhraseError('PHRASE COULD NOT BE FORGOTTEN.')


@as_dict()
def genie_share_your_knowledge():
    try:
        return db.session.query(Auth.id, Auth.comment).all()
    except OperationalError:
        raise PhraseError("COULD NOT SHARE THE GENIE'S KNOWLEDGE.")


## A TIP FOR ALL AND FOR ALL A GOOD TIP.

class QueryTipError(Exception):
    pass


class CramTipError(Exception):
    pass


class UpdateTipError(Exception):
    pass


class BulkUpdateTipError(UpdateTipError):
    def __init__(self, row):
        self.row = row


class SearchTipError(Exception):
    pass


def convert_patch_to_supported_values(patch):
    supported_ops = ['replace']
    supported_paths = ['/tweeted', '/approved']
    new_patch = []

    for oper in list(patch):
        if oper['op'] not in supported_ops:
            raise UpdateTipError('{0} OPERATION IS NOT SUPPORTED'.format(oper['op']))

        path = oper['path']

        if not any(path.endswith(supported) for supported in supported_paths):
            raise UpdateTipError('{0} IS NOT A SUPPORTED PATH'.format(path))

        if path.endswith('/tweeted'):
            try:
                oper['value'] = datetime.datetime.utcfromtimestamp(oper['value'])
            except Exception:
                # It wasn't worth converting anyway
                pass

        new_patch.append(oper)

    return jsonpatch.JsonPatch(new_patch)


class TipMaster(object):

    CROAK_SIZE = 50
    SUPER_SECRET_FIELDS = [Tip.approved, Tip.tweeted]

    def __init__(self):
        # OH GOD THE GLOBALS ARE LEAKING
        self.session = db.session

    @as_dict()
    def some_tips(self, super_secret_info=False, approved_only=True):
        try:
            query = self.tip_query(super_secret_info) \
                        .order_by(random())

            if approved_only:
                query = query.filter(Tip.approved == approved_only)

            return query.limit(self.CROAK_SIZE).all()
        except OperationalError:
            raise QueryTipError('TIP COULD NOT BE QUERIED.')

    @as_dict(single=True)
    def just_the_tip(self, number, super_secret_info=False, approved_only=True):
        try:
            query = self.tip_query(super_secret_info) \
                        .filter(Tip.number == number)

            if approved_only:
                query = query.filter(Tip.approved == approved_only) \

            return query.one_or_none()
        except OperationalError:
            raise QueryTipError('TIP COULD NOT BE QUERIED.')

    @as_dict()
    def search_for_spock(self, fat_filters):
        query = self.tip_query(super_secret_info=True)

        for key, value in fat_filters.items():
            if value is None:
                continue

            if key == 'tip':
                value = value.replace(' ', '%').upper()
                query = query.filter(Tip.tip.like('%{0}%'.format(value), escape='\\'))
            elif key == 'approved':
                query = query.filter(Tip.approved == value)
            elif key == 'tweeted':
                if value:
                    query = query.filter(Tip.tweeted != None)
                else:
                    query = query.filter(Tip.tweeted == None)

        try:
            return query.all()
        except OperationalError:
            raise SearchTipError('YOUR BIG DUMB CRITERIA COULD NOT BE SEARCHED FOR.')

    def cram_tip(self, text):
        session = self.session
        try:
            # SOME VERY IMPORTANT VERIFICATION
            if text.upper() != text:
                raise CramTipError('TIPS MUST BE IN UPPERCASE. HOW DID YOU NOT NOTICE THAT?')

            if not text.endswith('.'):
                raise CramTipError('TIPS MUST END WITH A FULL STOP. THIS THING --> .')

            if 'FROG' not in text:
                raise CramTipError('FROG TIPS MUST CONTAINS AT LEAST ONE MENTION OF THE TITULAR CHARACTER.')

            # YOU MADE IT!!!
            tip = Tip(tip=text, approved=False)
            session.add(tip)
            session.commit()
            return tip.number

        except OperationalError:
            raise CramTipError('COULD NOT ADD TIP.')

    def its_not_a_phase(self, number, patch):
        try:
            tip = self.session.query(Tip.number, Tip.tip, Tip.approved, Tip.tweeted) \
                              .filter(Tip.number == number) \
                              .one_or_none()

            if tip is None:
                raise UpdateTipError()

            tip = tip._asdict()
            new_patch = convert_patch_to_supported_values(patch)
            new_patch.apply(tip, in_place=True)

            self.session.query(Tip).filter(Tip.number == number).update(tip)
            self.session.commit()
        except OperationalError:
            raise UpdateTipError()

    def its_not_a_goth_phase(self, patch):
        updates = {}

        for oper in convert_patch_to_supported_values(patch):
            parts = oper['path'].split('/', 2)
            _, number, field = parts
            number = int(number)

            tip = updates.setdefault(number, {'number': number})
            tip.update({field: oper['value']})

        try:
            for row, tip in enumerate(updates.values()):
                try:
                    num_changed = self.session.query(Tip).filter(Tip.number == tip['number']).update(tip)
                    if num_changed != 1:
                        raise BulkUpdateTipError(row=row)

                except IntegrityError:
                    raise BulkUpdateTipError(row=row)

            self.session.commit()
        except OperationalError:
            raise UpdateTipError()

    def tip_query(self, super_secret_info):
        fields = [Tip.number, Tip.tip]

        if super_secret_info:
            fields.extend(self.SUPER_SECRET_FIELDS)

        return self.session.query(*fields)
