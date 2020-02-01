import xor
import hashes
import formats
from base64 import b64decode
import pymongo

def setup(ctx):
    app = ctx['app']
    db = ctx['db']
    get_arg = ctx['get_arg']
    get_user_str = ctx['get_user_str']

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