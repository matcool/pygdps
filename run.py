import os

os.environ['FLASK_APP'] = 'main.py'
os.environ['FLASK_ENV'] = 'development'

os.system('python -m flask run')