import hashlib

def hash_rewards(rewards_data: str) -> str:
    """
    Used in:
        - getGJRewards
    """
    return hashlib.sha1(bytes(rewards_data + 'pC26fpYaQCtg', 'utf-8')).hexdigest()

def hash_levels(levels) -> str:
    """
    Used in:
        - getGJLevels21
    """
    # '{first digit of level id}{last digit of level id}{stars}{starCoins?? 0 works fine So}'
    data = ''.join(f"{str(lvl['id'])[0]}{str(lvl['id'])[-1]}{lvl['stars']}0" for lvl in levels)
    return hashlib.sha1(bytes(data + 'xI25fpAapCQg', 'utf-8')).hexdigest()

def hash_mappack(mappacks) -> str:
    """
    Used in:
        - getGJMapPacks21
    """
    # '{first digit of mappack id}{last digit of mappack id}{coins}'
    data = ''.join(f"{str(mp['id'])[0]}{str(mp['id'])[-1]}{mp['stars']}{mp['coins']}" for mp in mappacks)
    return hashlib.sha1(bytes(data + 'xI25fpAapCQg', 'utf-8')).hexdigest()