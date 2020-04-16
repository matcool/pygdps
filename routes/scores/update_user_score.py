import xor
from typing import TYPE_CHECKING
if TYPE_CHECKING: from context import Context
import time
from flask import request
import json

class AccIcons:
    __slots__ = ('icon', 'ship', 'ball', 'ufo', 'wave', 'robot', 'spider', 'glow', 'explosion')

def setup(ctx: 'Context'):
    app = ctx.app
    db = ctx.db
    get_arg = ctx.get_arg

    @app.route('/updateGJUserScore.php', methods=['GET', 'POST'])
    @app.route('/updateGJUserScore19.php', methods=['GET', 'POST'])
    @app.route('/updateGJUserScore20.php', methods=['GET', 'POST'])
    @app.route('/updateGJUserScore21.php', methods=['GET', 'POST'])
    @app.route('/updateGJUserScore22.php', methods=['GET', 'POST'])
    def update_user_score():
        game_version = int(get_arg('gameVersion', 1))
        binary_version = int(get_arg('binaryVersion', 1))
        user_name = get_arg('userName')
        secret = get_arg('secret')
        if user_name is None or secret is None: return '-1'
        stars = int(get_arg('stars', 0))
        coins = int(get_arg('coins', 0))
        diamonds = int(get_arg('diamonds', 0))
        user_coins = int(get_arg('userCoins', 0))
        demons = int(get_arg('demons', 0))
        icon = int(get_arg('icon', 0))
        color1 = int(get_arg('color1', 0))
        color2 = int(get_arg('color2', 0))
        icon_type = int(get_arg('iconType', 0))
        special = int(get_arg('special', 0))

        ai = AccIcons() # great name
        for i in ('icon', 'ship', 'ball', 'ufo', 'wave', 'robot', 'spider', 'glow', 'explosion'):
            arg = 'acc' + i.capitalize()
            if i == 'ufo': arg = 'accBird'
            elif i == 'wave': arg = 'accDart'
            setattr(ai, i, int(get_arg(arg, 1)))
        
        acc_id = get_arg('accountID')
        ext_id = get_arg('udid')

        if acc_id is None and ext_id is None: return '-1'
        if ext_id is not None and ext_id.isnumeric(): return '-1'
        if acc_id:
            ext_id = int(acc_id)
            gjp = get_arg('gjp')
            if not ctx.check_acc_pw(ext_id, gjp):
                return '-1'
        else:
            register = False

        user_id = ctx.get_user_id(ext_id, user_name)

        # TODO: compare with old stats for some sort of "anticheat"

        db.users.find_one_and_update({'id': user_id}, {
            '$set': {
                'last_played': time.time(),
                'game_version': game_version,
                'name': user_name,
                'coins': coins,
                'diamonds': diamonds,
                'user_coins': user_coins,
                'secret': secret,
                'stars': stars,
                'demons': demons,
                'icon': icon,
                'color1': color1,
                'color2': color2,
                'icon_type': icon_type,
                'special': special,
                'acc_icon': ai.icon,
                'acc_ship': ai.ship,
                'acc_ball': ai.ball,
                'acc_ufo': ai.ufo,
                'acc_wave': ai.wave,
                'acc_robot': ai.robot,
                'acc_spider': ai.spider,
                'acc_glow': ai.glow,
                'acc_explosion': ai.explosion
            }
        })
        return str(user_id)
