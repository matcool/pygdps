from flask import Flask, request
import json
import os
from importlib import import_module
from context import Context
from colorama import init, Fore

app = Flask(__name__)

@app.route('/')
def root():
    return 'hi there'

@app.errorhandler(404)
def err(e):
    print(f'{Fore.YELLOW}Unhandled request! {Fore.LIGHTWHITE_EX}{request.path} {Fore.LIGHTBLACK_EX}{json.dumps(request.values.to_dict())}{Fore.RESET}')
    return '-1'

ctx = Context
ctx.app = app
init() # init colorama

for root, _, files in os.walk('routes'):
    for file in files:
        if not file.endswith('.py'): continue
        # this is very hacky but whatever
        path = os.path.join(root, file[:-3]).replace(os.sep, '.')
        print(f'{Fore.LIGHTBLACK_EX}Importing module: {Fore.RESET}{path}')
        import_module(path).setup(ctx)