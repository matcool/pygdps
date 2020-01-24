_level_search_values = ['id', 'name', 'description', None, 'version', 'user_id', None, 10, 'difficulty', 'downloads', None, 'audio_track', 'game_version', 'likes', 'length', None, 'demon', 'stars', 'featured', None, None, None, None, None, 'auto', None, None, None, None, 'original', 0, None, None, None, 'song_id', None, 'coins', 'star_coins', 'requested_stars', 'ldm', None, 'epic', 'demon_diff', None, 'objects', 1, 2]
def level_search(level) -> str:
    data = ''
    for i, key in enumerate(_level_search_values):
        i += 1 # it starts at 1 not 0
        if key is None: continue
        if type(key) is int: data += f'{i}:{key}:'
        else:
            val = level.get(key)
            if type(val) is bool: data += f'{i}:{int(val)}:' # turn bool into either 0 or 1
            else:                 data += f'{i}:{val or 0}:'
    print(data)
    return data[:-1] # remove left over :