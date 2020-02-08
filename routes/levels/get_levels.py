import xor
import hashes
import formats
from base64 import b64decode
import pymongo
from util import str_bool
import time
from typing import TYPE_CHECKING
if TYPE_CHECKING: from context import Context

def setup(ctx: 'Context'):
    app = ctx.app
    db = ctx.db
    get_arg = ctx.get_arg
    get_user_str = ctx.get_user_str

    bool_arg = lambda x: str_bool(get_arg(x))
    colon_arr = lambda x: tuple(map(int, x.split(',')))

    @app.route('/getGJLevels.php', methods=['GET', 'POST'])
    @app.route('/getGJLevels19.php', methods=['GET', 'POST'])
    @app.route('/getGJLevels20.php', methods=['GET', 'POST'])
    @app.route('/getGJLevels21.php', methods=['GET', 'POST'])
    def get_levels():
        query = {'unlisted': False}
        sort = [('likes', pymongo.DESCENDING)]

        game_version = int(get_arg('gameVersion', 0))

        if game_version == 20:
            binary_version = int(get_arg('binaryVersion'))
            if binary_version > 27: game_version += 1

        search_str = get_arg('str')
        search_type = int(get_arg('type', 0))
        if search_str and search_type == 0:
            if search_str.isnumeric():
                query.pop('unlisted') # ignore if level is unlisted or not
                query['id'] = int(search_str)
                sort = None
            else: query['name'] = {'$regex': search_str, '$options' : 'i'}
        
        query['game_version'] = {'$lte': 18 if game_version == 0 else game_version}

        if bool_arg('featured'): query['featured'] = True
        if bool_arg('epic'): query['epic'] = True
        if bool_arg('original'): query['original'] = 0
        if bool_arg('twoPlayer'): query['two_player'] = False
        if bool_arg('star'): query['stars'] = {'$ne': 0}
        if bool_arg('noStar'): query['stars'] = 0
        if bool_arg('coins'):
            query['coins'] = {'$ne': 0}
            query['rated_coins'] = True
        if get_arg('len', '-') != '-':
            lengths = int(get_arg('len'))
            query['length'] = {'$in': lengths}

        completed = bool_arg('onlyCompleted')
        if completed or bool_arg('uncompleted'):
            # for whatever reason its in a tuple-like format "(1,2,3)" instead of the usual "1,2,3"
            levels = colon_arr(get_arg('completedLevels')[1:-1])
            query['id'] = {('$in' if completed else '$nin'): levels}

        if get_arg('song'):
            song = int(get_arg('song'))
            if get_arg('customSong'):
                query['song_id'] = song
            else:
                query['audio_track'] = song - 1
                query['song_id'] = 0

        # TODO: difficulty filters

        if search_type and sort is not None:
            if search_type == 1:
                sort = [('downloads', pymongo.DESCENDING)]
            # skip search_type == 2 as sorting by likes is already the default
            elif search_type == 3:
                last_week = time.time() - (7 * 24 * 60 * 60)
                query['timestamp'] = {'$gt': last_week}
            elif search_type == 4:
                sort = [('id', pymongo.DESCENDING)]
            elif search_type == 5: # user levels
                sort = [('id', pymongo.DESCENDING)]
                query['user_id'] = int(search_str)
            elif search_type == 6: # featured
                query['featured'] = True
                # should be changed to rate date in the future
                sort = [('id', pymongo.DESCENDING)]
            elif search_type == 16: # hall of fame
                query['epic'] = True
                # should be changed to rate date in the future
                sort = [('id', pymongo.DESCENDING)]
            elif search_type == 7: # magic
                query['objects'] = {'$gt': 3000}
            elif search_type == 10: # mappacks
                sort = None
                query['id'] = {'$in': colon_arr(search_str)}

        page = int(get_arg('page', 0))
        per_page = 10
        offset = page * per_page

        levels = db.levels.find(query).skip(offset).limit(per_page)
        if sort: levels.sort(sort)
        levels = tuple(levels)

        data = '|'.join(map(formats.level_search, levels))
        
        users = []
        _users = set() # set of users already on the users array
        for level in levels:
            user_id = level['user_id']
            if user_id in _users: continue
            user = get_user_str(user_id)
            if user is None: continue
            users.append(user)
            _users.add(user_id)
        del _users
        users = '|'.join(users)

        songs = '' # placeholder

        return f'{data}#{users}#{songs}#{db.levels.count(query)}:{offset}:{per_page}#{hashes.hash_levels(levels)}'