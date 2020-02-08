import xor
import hashes
import formats
from base64 import b64encode
import pymongo
import time
from typing import TYPE_CHECKING
if TYPE_CHECKING: from context import Context

def setup(ctx: 'Context'):
    app = ctx.app
    db = ctx.db
    get_arg = ctx.get_arg
    get_user_id = ctx.get_user_id
    get_counter = ctx.get_counter
    check_acc_pw = ctx.check_acc_pw

    @app.route('/uploadGJLevel.php', methods=['GET', 'POST'])
    @app.route('/uploadGJLevel19.php', methods=['GET', 'POST'])
    @app.route('/uploadGJLevel20.php', methods=['GET', 'POST'])
    @app.route('/uploadGJLevel21.php', methods=['GET', 'POST'])
    def upload_level():
        timestamp = time.time()
        
        game_version = int(get_arg('gameVersion', 0))
        level_desc = get_arg('levelDesc', '')
        if game_version < 20:
            level_desc = b64encode(bytes(level_desc, 'utf-8')).decode('utf-8')

        level_data = get_arg('levelString')
        level_name = get_arg('levelName')
        if not level_data or not level_name: return '-1'

        user_name = get_arg('userName')
        
        ext_id = get_arg('udid')
        if ext_id is not None and ext_id.isnumeric():
            return '-1'

        gjp = get_arg('gjp')
        acc_id = get_arg('accountID')
        if acc_id and acc_id != '0':
            ext_id = int(acc_id)
            gjp = get_arg('gjp')
            if not check_acc_pw(ext_id, gjp):
                return '-1'

        user_id = get_user_id(ext_id, user_name)

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
            'user_id': user_id,
            'ext_id': ext_id,
            'unlisted': bool(int(get_arg('unlisted', False))),
            'ldm': bool(int(get_arg('ldm', False))),
            # online stuff
            'downloads': 0,
            'likes': 0,
            'difficulty': 0, # 0=N/A 10=EASY 20=NORMAL 30=HARD 40=HARDER 50=INSANE 50=AUTO 50=DEMON
            # for some reason setting difficulty >= 60 seems to also be a demon, even though its supposed to use the a demon boolean
            # although there doesnt seem to be some difficulty value for auto, that actually needs to use the auto boolean value
            'demon': False,
            'demon_diff': 0, # 1=easy 2=medium 3=hard 4=insane 5=extreme demon
            'stars': 0,
            'featured': False,
            'epic': False,
            'rated_coins': False
        })
        return str(level_id)
