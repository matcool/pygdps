import xor
from typing import TYPE_CHECKING
if TYPE_CHECKING: from context import Context
import time
from flask import request
import formats
import random

def setup(ctx: 'Context'):
    app = ctx.app
    db = ctx.db
    get_arg = ctx.get_arg

    @app.route('/getGJUserInfo20.php', methods=['GET', 'POST'])
    def get_user_info():
        ext_id = get_arg('targetAccountID')
        acc_id = get_arg('accountID')
        me = 0 # great naming
        if acc_id:
            me = int(acc_id)
            if not ctx.check_acc_pw(me, get_arg('gjp')):
                return '-1'
        if ext_id.isnumeric():
            ext_id = int(ext_id)
        user = db.users.find_one({'ext_id': ext_id})
        if user is None: return '-1'

        # placeholders
        # TODO: do whatever cvolton does for these https://github.com/Cvolton/GMDprivateServer/blob/master/incl/profiles/getGJUserInfo.php
        creator_points = 0
        rank = 1
        freq_state = 0
        msg_state = 0
        comment_state = 0
        badge = 0
        friend_requests = 0
        messages = 0
        friends = 0
        friend_state = 0
        if False: # enable for some fun
            user.update({
                'acc_icon': random.randint(0, 142),
                'acc_ship': random.randint(0, 51),
                'acc_ball': random.randint(0, 43),
                'acc_wave': random.randint(0, 35),
                'acc_ufo': random.randint(0, 35),
                'acc_robot': random.randint(0, 26),
                'acc_spider': random.randint(0, 17),
                'color1': random.randint(0, 42),
                'color2': random.randint(0, 42),
                'acc_glow': 0
            })
        return formats.get_user_info(user, {
            'creator_points': creator_points,
            'msg_state': msg_state,
            'freq_state': freq_state,
            'comment_state': comment_state,
            'rank': rank,
            'badge': badge,
            'youtube': '',
            'twitter': '',
            'twitch': '',
            'pms': messages,
            'requests': friend_requests,
            'friends': friends
        })
