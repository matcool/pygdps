import xor
import hashes
import formats
from base64 import b64decode
import pymongo

def setup(ctx):
    app = ctx['app']
    db = ctx['db']
    get_arg = ctx['get_arg']

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