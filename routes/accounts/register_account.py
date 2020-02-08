import time
from typing import TYPE_CHECKING
if TYPE_CHECKING: from context import Context

def setup(ctx: 'Context'):
    app = ctx.app
    db = ctx.db
    get_arg = ctx.get_arg
    get_counter = ctx.get_counter
    pw_hasher = ctx.pw_hasher

    @app.route('/accounts/registerGJAccount.php', methods=['GET', 'POST'])
    def register_account():
        user_name = get_arg('userName')
        password = get_arg('password')
        email = get_arg('email')
        if not user_name or not password or not email:
            return '-1'
        secret = get_arg('secret')
        
        # account with same name already exists
        if db.accounts.count({'name': user_name}):
            return '-2'
        
        db.accounts.insert_one({
            'id': get_counter('accounts'),
            'name': user_name,
            'password': pw_hasher.hash(password),
            'email': email,
            'timestamp': time.time(),
            'secret': secret,
            'save_data': b'',
            'save_key': b''
        })
        return '1'