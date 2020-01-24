from flask import Flask, request
from base64 import b64encode
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
    'levels': '1',
    'stars': 10,
    'coins': 5,
    'difficulty': 2,
    'color': '20,0,255'
}]

# TODO: this somehow broke after switching to mongodb??
@app.route('/getGJMapPacks21.php', methods=['GET', 'POST'])
def get_mappacks():
    page = int(get_arg('page', 0))

    mappack_data = ''
    mappack_ids = ''

    for mappack in MAPPACKS:
        mappack_ids += f"{mappack['id']},"
        mappack_data += f"1:{mappack['id']}:2:{mappack['name']}:" \
                        f"3:{mappack['levels']}:4:{mappack['stars']}:" \
                        f"5:{mappack['coins']}:" \
                        f"6:{mappack['difficulty']}:7:{mappack['color']}:8:{mappack['color']}|"

    mappack_data = mappack_data[:-1]
    mappack_ids = mappack_ids[:-1]

    return f'{mappack_data}#{len(MAPPACKS)}:0:10#{hashes.hash_mappack(MAPPACKS)}'

@app.route('/getGJLevels21.php', methods=['GET', 'POST'])
def get_levels():
    search_type = int(get_arg('type', 0))

    # TODO: additional search types (featured, original, etc)

    data = get_arg('str')

    level_ids = ''
    result = ''
    users = ''

    levels = tuple(db.levels.find({}))
    for lvl in levels:
        level_ids += f"{lvl['id']},"
        result += formats.level_search(lvl) + '|'
        users += f"16:mat:0|"
    
    level_ids = level_ids[:-1]
    result = result[:-1]
    users = users[:-1]

    songs = ''

    return f'{result}#{users}#{songs}#{len(levels)}:0:10#{hashes.hash_levels(levels)}'

@app.route('/uploadGJLevel21.php', methods=['GET', 'POST'])
def upload_level():
    timestamp = time.time()
    
    game_version = int(get_arg('gameVersion', 0))
    binary_version = int(get_arg('binaryVersion', 0))
    username = get_arg('userName')
    level_id = get_arg('levelID')
    level_name = get_arg('levelName')
    level_desc = get_arg('levelDesc')
    if game_version < 20:
        level_desc = b64encode(bytes(level_desc, 'utf-8')).decode('utf-8')
    level_version = int(get_arg('levelVersion'))
    level_length = int(get_arg('levelLength'))
    audio_track = int(get_arg('audioTrack'))

    auto = bool(int(get_arg('auto', False)))
    original = int(get_arg('original', 0))
    two_player = bool(int(get_arg('twoPlayer', False)))
    song_id = int(get_arg('songID', 0))
    objects = int(get_arg('objects', 0))
    coins = int(get_arg('coins', 0))
    requested_stars = int(get_arg('requestedStars', 0))
    unlisted = bool(int(get_arg('unlisted', False)))
    ldm = bool(int(get_arg('ldm', False)))
    
    password = get_arg('password', 1)
    if game_version > 17: password = 0
    password = int(password)

    level_data = get_arg('levelString')
    extra_data = get_arg('extraString', '29_29_29_40_29_29_29_29_29_29_29_29_29_29_29_29')
    level_info = get_arg('levelInfo', 0)
    secret = get_arg('secret')

    if not level_data or not level_name: return '-1'
    
    udid = get_arg('udid')
    if udid is not None and udid.isnumeric():
        return '-1'

    gjp = get_arg('gjp')
    account_id = get_arg('accountID')
    # wont run if its None or 0
    if account_id:
        # check if account id matches gjp
        # currently no account system, so always fail
        return '-1'

    level_id = get_counter('levels')

    db.levels.insert_one({
        'name': level_name,
        'id': level_id,
        'level_data': level_data,
        'extra_data': extra_data,
        'level_info': level_info,
        'timestamp': timestamp,
        'description': level_desc,
        'game_version': game_version,
        'binary_version': binary_version,
        'username': username,
        'version': level_version,
        'length': level_length,
        # difference between audio_track and song_id is
        # audio_track is official songs and song_id is newgrounds aka custom songs
        'audio_track': audio_track,
        'song_id': song_id,
        'auto': auto,
        'password': password,
        'original': original,
        'two_player': two_player,
        'objects': objects,
        'coins': coins,
        'requested_stars': requested_stars,
        'secret': secret,
        'user_id': -1, # no user_id yet
        'udid': udid, #??? i have no idea what this is
        'unlisted': unlisted,
        'ldm': ldm,
        # online stuff
        'downloads': 0,
        'likes': 0,
        'difficulty': 0, # 0=N/A 10=EASY 20=NORMAL 30=HARD 40=HARDER 50=INSANE 50=AUTO 50=DEMON
        'stars': 0,
        'demon': False,
        'featured': False,
        'epic': False
    })
    return str(level_id)