from flask import Flask, request
import json
import hashes
import formats

app = Flask(__name__)

"""
set FLASK_APP=main.py
set FLASK_ENV=development
flask run
"""

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
from context import Context

ctx = Context
ctx.app = app

for root, _, files in os.walk('routes'):
    for file in files:
        if not file.endswith('.py'): continue
        # this is very hacky but whatever
        path = os.path.join(root, file[:-3]).replace(os.sep, '.')
        print(f'Importing module: {path}')
        import_module(path).setup(ctx)