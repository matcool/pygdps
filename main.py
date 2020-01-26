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

@app.route('/getGJLevels21.php', methods=['GET', 'POST'])
def get_levels():
    query = {}
    sort = [('likes', pymongo.DESCENDING)]

    search_str = get_arg('str')
    search_type = int(get_arg('type', 0))
    if search_str and search_type == 0:
        if search_str.isnumeric():
            query['id'] = int(search_str)
            sort = None
        else: query['name'] = {'$regex': search_str, '$options' : 'i'}

    if search_type and sort is not None:
        if search_type == 1:
            sort = [('downloads', pymongo.DESCENDING)]
        # skip search_type == 2 as sorting by likes is already the default
        elif search_type == 3:
            last_week = time.time() - (7 * 24 * 60 * 60)
            query['timestamp'] = {'$gt': last_week}
        elif search_type == 4:
            sort = [('id', pymongo.DESCENDING)]
        elif search_type == 7: # magic
            sort = query['objects'] = {'$gt', 3000}
        elif search_type == 10: # mappacks
            sort = None
            query['id'] = {'$in': list(map(int, search_str.split(',')))}

    page = int(get_arg('page', 0))
    per_page = 10
    offset = page * per_page

    levels = db.levels.find(query).skip(offset).limit(per_page)
    if sort: levels.sort(sort)
    levels = tuple(levels)

    data = '|'.join(map(formats.level_search, levels))
    
    users = '16:mat:0' # placeholder

    songs = '' # placeholder

    return f'{data}#{users}#{songs}#{db.levels.count(query)}:{offset}:{per_page}#{hashes.hash_levels(levels)}'

@app.route('/uploadGJLevel21.php', methods=['GET', 'POST'])
def upload_level():
    timestamp = time.time()
    
    game_version = int(get_arg('gameVersion', 0))
    level_desc = get_arg('levelDesc')
    if game_version < 20:
        level_desc = b64encode(bytes(level_desc, 'utf-8')).decode('utf-8')

    level_data = get_arg('levelString')
    level_name = get_arg('levelName')
    if not level_data or not level_name: return '-1'
    
    udid = get_arg('udid')
    if udid is not None and udid.isnumeric():
        return '-1'

    gjp = get_arg('gjp')
    account_id = get_arg('accountID')
    if account_id:
        # check if account id matches gjp
        # currently no account system, so always fail
        return '-1'

    level_id = get_counter('levels')

    db.levels.insert_one({
        'name': level_name,
        'id': level_id,
        'data': level_data,
        'extra_data': get_arg('extraString', '29_29_29_40_29_29_29_29_29_29_29_29_29_29_29_29'),
        'info': get_arg('levelInfo', 0),
        'timestamp': time.time(),
        'description': level_desc,
        'game_version': game_version,
        'binary_version': int(get_arg('binaryVersion', 0)),
        'username': get_arg('userName'),
        'version': int(get_arg('levelVersion')),
        'length': int(get_arg('levelLength')),
        # difference between audio_track and song_id is
        # audio_track is official songs and song_id is newgrounds aka custom songs
        'audio_track': int(get_arg('audioTrack')),
        'song_id': int(get_arg('songID', 0)),
        # gd seems to detect if a level is auto or not, based on the number of jumps when you verify a level
        'auto': bool(int(get_arg('auto', False))),
        'password': int(get_arg('password', 0 if game_version > 17 else 1)),
        'original': int(get_arg('original', 0)),
        'two_player': bool(int(get_arg('twoPlayer', False))),
        'objects': int(get_arg('objects', 0)),
        'coins': int(get_arg('coins', 0)),
        'requested_stars': int(get_arg('requestedStars', 0)),
        'secret': get_arg('secret'),
        'user_id': -1, # no user_id yet
        'udid': udid, #??? i have no idea what this is
        'unlisted': bool(int(get_arg('unlisted', False))),
        'ldm': bool(int(get_arg('ldm', False))),
        # online stuff
        'downloads': 0,
        'likes': 0,
        'difficulty': 0, # 0=N/A 10=EASY 20=NORMAL 30=HARD 40=HARDER 50=INSANE 50=AUTO 50=DEMON
        # for some reason setting difficulty >= 60 seems to also be a demon, even though its supposed to use the a demon boolean
        # although there doesnt seem to be some difficulty value for auto, that actually needs to use the auto boolean value
        'demon': False,
        'demon_diff': 0 # 1=easy 2=medium 3=hard 4=insane 5=extreme demon
        'stars': 0,
        'featured': False,
        'epic': False,
        'rated_coins': False,
    })
    return str(level_id)

@app.route('/downloadGJLevel22.php', methods=['GET', 'POST'])
def download_level():
    game_version = int(get_arg('gameVersion', 1))
    level_id = get_arg('levelID')
    if level_id is None: return '-1'
    try:
        level_id = int(level_id)
    except ValueError:
        return '-1'
    
    level = db.levels.find_one_and_update({'id': level_id}, {'$inc': {'downloads': 1}}, return_document=pymongo.ReturnDocument.AFTER)
    if level is None: return '-1'

    password = level['password']
    description = level['description']
    
    xor_pw = password
    if game_version > 19:
        if password != 0:
            xor_pw = xor.encode(str(password), '26364')
    else:
        description = b64decode(bytes(description, 'utf-8')).decode('utf-8')
    
    level_data = level['data']

    if game_version > 18 and level_data.startswith('kS1'):
        return '-1' # too lazy to do the gzcompress stuff rn

    result = formats.level_download(level, {
        'description': description,
        'data': level_data,
        'password': xor_pw,
        'upload_date': 'placeholder', # on latest gd ver these seem to be broken no matter what
        'update_date': 'placeholder'
    })

    result += f'#{hashes.hash_level(level_data)}#'
    extra_data = ','.join(str(int(level.get(key, 0))) for key in ('user_id','stars','demon','id','rated_coins','featured'))
    extra_data += f',{password},{0}' # 0 is featured id
    result += f'{hashes.hash_solo2(extra_data)}#{extra_data}'

    return result