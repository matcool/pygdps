from argon2 import PasswordHasher
from flask import Flask, request
from typing import Union
import pymongo
import xor
import time

class Context():
    """Contain values and functions that are used in routes"""
    app: Flask = None
    db_client = pymongo.MongoClient()
    db = db_client.gdps

    @staticmethod
    def get_arg(name: str, default: bool=None) -> str:
        return request.values.get(name, default)

    @staticmethod
    def get_counter(name: str) -> int:
        doc = Context.db.counters.find_one_and_update(
            {'_id': name},
            {'$inc': {'value': 1}},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER
        )
        return doc['value']

    @staticmethod
    def get_user_id(ext_id: Union[int, str], user_name: str) -> int:
        registered = isinstance(ext_id, int)

        user = Context.db.users.find_one({'ext_id': ext_id}, ['id'])
        if user: return user['id']
        user_id = Context.get_counter('users')
        user = Context.db.users.insert_one({
            'name': user_name,
            'id': user_id,
            'ext_id': ext_id,
            'timestamp': time.time(),
            'registered': registered
        })
        return user_id

    @staticmethod
    def get_user_str(user_id: int) -> str:
        user = Context.db.users.find_one({'id': user_id})
        if user is None: return None
        ext_id = user['ext_id'] if type(user['ext_id']) == int else 0
        return f"{user_id}:{user['name']}:{ext_id}"

    pw_hasher = PasswordHasher()

    @staticmethod
    def check_acc_pw(acc_id: int, gjp_pw: str) -> bool:
        password = xor.decode(gjp_pw, xor.GJP_KEY)
        account = Context.db.accounts.find_one({'id': acc_id}, ['password'])
        if account is None: return False
        try:
            Context.pw_hasher.verify(account.get('password'), password)
        except Exception:
            return False
        return True