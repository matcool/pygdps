from flask import Flask, request
from base64 import b64encode
import xor
import time
import random
import hashes
import json
import pymongo
import hashes

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

LEVELS = [
    {
        'id': 1,
        'name': 'I am awesome level',
        'star_diff': 20,
        'downloads': 20,
        'likes': 30,
        'song': 0,
        'stars': 5,
        'description': 'An awesome level!!!!',
        'length': 0,
        'author': 16
    },
    {
        'id': 2,
        'name': 'SECOND',
        'star_diff': 10,
        'downloads': 20,
        'likes': 30,
        'song': 3,
        'stars': 5,
        'description': 'An awesome level!!!!',
        'length': 0,
        'author': 16
    },
    {
        'id': 3,
        'name': '333',
        'star_diff': 60,
        'downloads': 333,
        'likes': 333,
        'song': 3,
        'stars': 333,
        'description': 'An awesome level!!!!',
        'length': 0,
        'author': 16
    }
]

@app.route('/getGJLevels21.php', methods=['GET', 'POST'])
def get_levels():
    search_type = int(get_arg('type', 0))

    # TODO: additional search types (featured, original, etc)

    data = get_arg('str')

    level_ids = ''
    result = ''
    users = ''

    levels = tuple(db.levels.find({}))
    # for lvl in LEVELS:
    for lvl in levels:
        level_ids += f"{lvl['id']},"
        # "1:".$level1["levelID"].":2:".$level1["levelName"].":5:".$level1["levelVersion"].":6:".$level1["userID"].":8:10:9:".$level1["starDifficulty"].":10:".$level1["downloads"].":12:".$level1["audioTrack"].":13:".$level1["gameVersion"].":14:".$level1["likes"].":17:".$level1["starDemon"].":43:".$level1["starDemonDiff"].":25:".$level1["starAuto"].":18:".$level1["starStars"].":19:".$level1["starFeatured"].":42:".$level1["starEpic"].":45:".$level1["objects"].":3:".$level1["levelDesc"].":15:".$level1["levelLength"].":30:".$level1["original"].":31:0:37:".$level1["coins"].":38:".$level1["starCoins"].":39:".$level1["requestedStars"].":46:1:47:2:40:".$level1["isLDM"].":35:".$level1["songID"]."|";
        result += f"1:{lvl['id']}:2:{lvl['name']}:5:0:6:16:8:10:9:{lvl['difficulty']}:10:{lvl['downloads']}:12:{lvl['audio_track']}:13:21:14:{lvl['likes']}:17:0:43:0:25:0:18:{lvl['stars']}:19:0:42:0:45:10:3:{lvl['description']}:15:{lvl['length']}:30:0:31:0:37:0:38:0:39:0:46:1:47:2:40:0:35:{lvl['song_id']}|"
        users += f"16:mat:0|"
    
    level_ids = level_ids[:-1]
    result = result[:-1]
    users = users[:-1]

    songs = ''

    return f'{result}#{users}#{songs}#{len(levels)}:0:10#{hashes.hash_levels(levels)}'

@app.route('/uploadGJLevel21.php', methods=['GET', 'POST'])
def upload_level():
    # Unhandled request! /uploadGJLevel21.php {"gameVersion": "21", "binaryVersion": "35", "gdw": "0", "udid": "S1521127215430553004070531048977861003", "uuid": "0", "userName": "WESOME", "levelID": "0", "levelName": "asd", "levelDesc": "", "levelVersion": "1", "levelLength": "0", "audioTrack": "0", "auto": "0", "password": "0", "original": "0", "twoPlayer": "0", "songID": "0", "objects": "8", "coins": "0", "requestedStars": "5", "unlisted": "0", "wt": "3", "wt2": "0", "ldm": "0", "extraString": "0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0", "seed": "VTUjESg6pc", "seed2": "UQEKD1IHAAdRAQQDUQUBAgJRBFJVVVZSAwEGA1MDAwkLBwJVBgsBUA==", "levelString": "H4sIAAAAAAAAC6WQ0Q3CMAxEFzKSz4nTVnx1hg5wA3QFhqeJqQQihSJ-7nKX-MnKuqRRwKw0wpyJ5k4gzMKizLyAhVBVDgThVUYqR-IGNoTaOQT-R0xdRH0TA6cgxjrfA9Xf2EH6DeOHGP1lm3KAkXVGEq3mYSUsy6ZxHqJ52FhtSVNL1jQA7WLOTeMWGgbRKwRiAnVJAt9jiii2ZdX8Uue3uvTr6UM99Ou6Rw_-3N8BtWYqi8ECAAA=", "levelInfo": "H4sIAAAAAAAACyXLwQ0AIAgDwI0IIAqm--9lwQ_tpUEBFU0YIxdgYpswcW_sNThcnM1Fi03iIwaVg5tA9W64_cdbATxRWWGYYQAAAA==", "secret": "Wmfd2893gb7"}
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

    auto = bool(get_arg('auto', False))
    original = int(get_arg('original', 0))
    two_player = bool(get_arg('twoPlayer', False))
    song_id = int(get_arg('songID', 0))
    objects = int(get_arg('objects', 0))
    coins = int(get_arg('coins', 0))
    requested_stars = int(get_arg('requestedStars', 0))
    unlisted = bool(get_arg('unlisted', False))
    ldm = bool(get_arg('ldm', False))
    
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
    
#$query = $db->prepare("INSERT INTO levels (levelName, gameVersion, binaryVersion, userName, levelDesc, levelVersion, levelLength, audioTrack, auto, password, original, twoPlayer, songID, objects, coins, requestedStars, extraString, levelString, levelInfo, secret, uploadDate, userID, extID, updateDate, unlisted, hostname, isLDM)
#VALUES (:levelName, :gameVersion, :binaryVersion, :userName, :levelDesc, :levelVersion, :levelLength, :audioTrack, :auto, :password, :original, :twoPlayer, :songID, :objects, :coins, :requestedStars, :extraString, :levelString, :levelInfo, :secret, :uploadDate, :userID, :id, :uploadDate, :unlisted, :hostname, :ldm)");


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
    })
    # $query->execute([':levelName' => $levelName, ':gameVersion' => $gameVersion, ':binaryVersion' => $binaryVersion, ':userName' => $userName, ':levelDesc' => $levelDesc, ':levelVersion' => $levelVersion, ':levelLength' => $levelLength, ':audioTrack' => $audioTrack, ':auto' => $auto, ':password' => $password, ':original' => $original, ':twoPlayer' => $twoPlayer, ':songID' => $songID, ':objects' => $objects, ':coins' => $coins, ':requestedStars' => $requestedStars, ':extraString' => $extraString, ':levelString' => "", ':levelInfo' => $levelInfo, ':secret' => $secret, ':uploadDate' => $uploadDate, ':userID' => $userID, ':id' => $id, ':unlisted' => $unlisted, ':hostname' => $hostname, ':ldm' => $ldm]);
    return str(level_id)