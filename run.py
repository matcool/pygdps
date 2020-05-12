import os
from colorama import Fore

os.environ['FLASK_APP'] = 'main.py'
os.environ['FLASK_ENV'] = 'development'

try:
    os.system('flask run')
except KeyboardInterrupt:
    print(f'{Fore.RED}CTRL+C pressed, exiting{Fore.RESET}')
