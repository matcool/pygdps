# PyGDPS [WIP]
Geometry dash Private server written in python using Flask and MongoDB, highly based off [Cvolton/GMDprivateServer](https://github.com/Cvolton/GMDprivateServer)

## Running
Needs a local mongodb server running (no current way to change address)
### Linux
```bash
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```
### Windows
```batch
set FLASK_APP=main.py
set FLASK_ENV=development
flask run
```

## Implemented
- `/uploadGJLevel.php` - uploading a level works, and thats it (no replacing already uploaded level, etc)
- `/getGJLevels.php` - searching by difficulty is missing
- `/getGJMapPacks.php` - mappacks are not yet stored in the db
- `/downloadGJLevel.php` - daily levels dont work yet
- `/accounts/registerGJAccount.php` - nothing much to say, it works (passwords are argon2 hashed)
- `/accounts/loginGJAccount.php` - same as above
- `/updateGJUserScore.php` - works fine
- `/getGJUserInfo.php` - works fine but creator points, rank and etc are hardcoded