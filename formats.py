_level_search_keys = ['id', 'name', 'description', None, 'version', 'user_id', None, 10, 'difficulty', 'downloads', None, 'audio_track', 'game_version', 'likes', 'length', None, 'demon', 'stars', 'featured', None, None, None, None, None, 'auto', None, None, None, None, 'original', 0, None, None, None, 'song_id', None, 'coins', 'rated_coins', 'requested_stars', 'ldm', None, 'epic', 'demon_diff', None, 'objects', 1, 2]
def level_search(level) -> str:
    data = ''
    for i, key in enumerate(_level_search_keys):
        i += 1 # it starts at 1 not 0
        if key is None: continue
        if type(key) is int: data += f'{i}:{key}:'
        else:
            val = level.get(key)
            if type(val) is bool: data += f'{i}:{int(val)}:' # turn bool into either 0 or 1
            else:                 data += f'{i}:{val or 0}:'
    return data[:-1] # remove left over :

_mappack_keys = ['id', 'name', 'levels', 'stars', 'coins', 'difficulty', 'color', 'color']
def mappack(mp) -> str:
    return ':'.join(f'{i + 1}:{mp.get(key, 0)}' for i, key in enumerate(_mappack_keys))

_level_download_keys = ['id', 'name', '!description', '!data', 'version', 'user_id', None, 10, 'difficulty', 'downloads', 1, 'audio_track', 'game_version', 'likes', 'length', None, 'demon', 'stars', 'featured', None, None, None, None, None, 'auto', None, '!password', '!upload_date', '!update_date', 'original', 1, None, None, None, 'song_id', 'extra_data', 'coins', 'rated_coins', 'requested_stars', 'ldm', None, 'epic', 'demon_diff', None, 'objects', 1, 2, 1]
def level_download(level, extra) -> str:
    data = ''
    for i, key in enumerate(_level_download_keys):
        i += 1 # it starts at 1 not 0
        if key is None: continue
        if type(key) is int: data += f'{i}:{key}:'
        else:
            if key[0] == '!': val = extra.get(key[1:])
            else:             val = level.get(key)
            if type(val) is bool: data += f'{i}:{int(val)}:' # turn bool into either 0 or 1
            else:                 data += f'{i}:{val or 0}:'
    return data[:-1] # remove left over :