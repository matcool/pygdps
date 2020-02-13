from flask import Flask, request
import json
import os
from importlib import import_module
from context import Context

app = Flask(__name__)

@app.route('/')
def root():
    return 'hi there'

@app.errorhandler(404)
def err(e):
    print(f'Unhandled request! {request.path} {json.dumps(request.values.to_dict())}')
    return '-1'

ctx = Context
ctx.app = app

for root, _, files in os.walk('routes'):
    for file in files:
        if not file.endswith('.py'): continue
        # this is very hacky but whatever
        path = os.path.join(root, file[:-3]).replace(os.sep, '.')
        print(f'Importing module: {path}')
        import_module(path).setup(ctx)