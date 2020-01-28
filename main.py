from flask import Flask, request
from base64 import b64encode, b64decode
import xor
import time
import random
import hashes
import json
import pymongo
import hashes
import formats

app = Flask(__name__)
db_client = pymongo.MongoClient()
db = db_client.gdps

"""
set FLASK_APP=main.py
set FLASK_ENV=development
flask run
"""

def get_arg(name: str, default: bool=None) -> str:
    return request.values.get(name, default)

def get_counter(name: str) -> int:
    doc = db.counters.find_one_and_update(
        {'_id': name},
        {'$inc': {'value': 1}},
        upsert=True,
        return_document=pymongo.ReturnDocument.AFTER
    )
    return doc['value']

def get_user_id(ext_id: str, user_name: str) -> int:
    registered = ext_id.isnumeric()

    user = db.users.find_one({'ext_id': ext_id}, ['id'])
    if user: return user['id']
    user_id = get_counter('users')
    user = db.users.insert_one({
        'name': user_name,
        'id': user_id,
        'ext_id': ext_id,
        'timestamp': time.time(),
        'registered': registered
    })
    return user_id

def get_user_str(user_id: int) -> str:
    user = db.users.find_one({'id': user_id})
    if user is None: return None
    ext_id = user['ext_id'] if user['ext_id'].isnumeric() else 0
    return f"{user_id}:{user['name']}:{ext_id}"

@app.route('/')
def root():
    return 'hi there'

@app.errorhandler(404)
def err(e):
    print(f'Unhandled request! {request.path} {json.dumps(request.values.to_dict())}')
    return '-1'

MAPPACKS = [{
    'id': 1,
    'name': 'Awesome',
    'levels': '1,2',
    'stars': 10,
    'coins': 5,
    'difficulty': 2,
    'color': '20,0,255'
}]

@app.route('/getGJMapPacks21.php', methods=['GET', 'POST'])
def get_mappacks():
    data = '|'.join(map(formats.mappack, MAPPACKS))
    return f'{data}#{len(MAPPACKS)}:0:10#{hashes.hash_mappack(MAPPACKS)}'

import os
from importlib import import_module

ctx = locals() # temp

for root, _, files in os.walk('routes'):
    for file in files:
        if not file.endswith('.py'): continue
        # this is very hacky but whatever
        path = os.path.join(root, file[:-3]).replace(os.sep, '.')
        print(f'Importing module: {path}')
        import_module(path).setup(ctx)