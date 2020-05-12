import os

os.environ['FLASK_APP'] = 'main.py'
os.environ['FLASK_ENV'] = 'development'

try:
    os.system('flask run')
except KeyboardInterrupt:
    pass
