from typing import List, Union, Callable, Optional
from util import bool_str

class Skip:
    __slots__ = ('n',)
    def __init__(self, n: int):
        self.n = n

def format_function(keys: List[Union[str, Skip, None]]) -> Callable[[dict, Optional[dict]], str]:
    def wrapper(obj, extra={}):    
        data = ''
        skipped = 0
        
        for i, key in enumerate(keys):
            i += 1 + skipped # robtop counts from 1
            if key is None: continue
            elif isinstance(key, Skip):
                skipped += key.n - 1
            elif type(key) is int:
                data += f'{i}:{key}:'
            else:
                if key[0] == '!':
                    val = extra.get(key[1:])
                else:
                    val = obj.get(key)
                
                if type(val) is bool:
                    data += f'{i}:{bool_str(val)}:'
                elif isinstance(val, str) and not val:
                    data += f'{i}::'
                else:
                    data += f'{i}:{val or 0}:'
        return data[:-1]
    return wrapper

_mappack_keys = ['id', 'name', 'levels', 'stars', 'coins', 'difficulty', 'color', 'color']
def mappack(mp) -> str:
    return ':'.join(f'{i + 1}:{mp.get(key, 0)}' for i, key in enumerate(_mappack_keys))

level_search = format_function(['id', 'name', 'description', None, 'version', 'user_id', None, 10, 'difficulty', 'downloads', None, 'audio_track', 'game_version', 'likes', 'length', None, 'demon', 'stars', 'featured', Skip(5), 'auto', Skip(4), 'original', 0, Skip(3), 'song_id', None, 'coins', 'rated_coins', 'requested_stars', 'ldm', None, 'epic', 'demon_diff', None, 'objects', 1, 2])

level_download = format_function(['id', 'name', '!description', '!data', 'version', 'user_id', None, 10, 'difficulty', 'downloads', 1, 'audio_track', 'game_version', 'likes', 'length', None, 'demon', 'stars', 'featured', Skip(5), 'auto', None, '!password', '!upload_date', '!update_date', 'original', 1, Skip(3), 'song_id', 'extra_data', 'coins', 'rated_coins', 'requested_stars', 'ldm', None, 'epic', 'demon_diff', None, 'objects', 1, 2, 1])

get_user_info = format_function(['name', 'id', 'stars', 'demons', Skip(3), '!creator_points', None, 'color1', 'color2', None, 'coins', Skip(2), 'ext_id', 'user_coins', '!msg_state', '!freq_state', '!youtube', 'acc_icon', 'acc_ship', 'acc_ball', 'acc_ufo', 'acc_wave', 'acc_robot', None, 'acc_glow', 1, '!rank', '!friend_state', Skip(6), '!pms', '!requests', '!friends', Skip(2), 'acc_spider', '!twitter', '!twitch', 'diamonds', 'acc_explosion', None, '!badge', '!comment_state'])
