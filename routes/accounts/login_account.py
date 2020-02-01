import xor
from argon2 import PasswordHasher
import time

def setup(ctx):
    app = ctx['app']
    db = ctx['db']
    get_arg = ctx['get_arg']
    get_counter = ctx['get_counter']
    pw_hasher = PasswordHasher()

    @app.route('/accounts/loginGJAccount.php', methods=['GET', 'POST'])
    def login_account():
        user_name = get_arg('userName')
        password = get_arg('password')
        udid = get_arg('udid')

        account = db.accounts.find_one({'name': user_name})

        encrypted_pw = account.get('password')

        # dumb library errors instead of returning False so i have to do this
        try:
            pw_hasher.verify(encrypted_pw, password)
        except Exception:
            return '-1'

        acc_id = account.get('id')

        user = db.users.find_one({'ext_id': acc_id}, ['id'])
        if user:
            user_id = user['id']
        else:
            user_id = get_counter('users')
            db.users.insert_one({
                'name': user_name,
                'id': user_id,
                'ext_id': acc_id,
                'registered': True,
                'timestamp': time.time()
            })
        
        # transfer levels to account
        if not udid.isnumeric():
            old_user_id = db.users.find_one({'ext_id': udid}, ['id']).get('id')
            db.levels.update_many(
                {'user_id': old_user_id},
                {
                    '$set': {
                        'user_id': user_id,
                        'ext_id': acc_id
                    }
                }
            )

        return f'{acc_id},{user_id}'
