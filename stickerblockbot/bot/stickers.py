from . import config

config_name = "banned_stickers"

banned_packs = {}


def init():
    global banned_packs
    pack_list = config.get(config_name)
    if pack_list is None or type(pack_list).__name__ != "list":
        banned_packs = {}
    else:
        for pack in pack_list:
            banned_packs[pack] = True


def save_bans():
    pack_list = []
    for pack in banned_packs.keys():
        pack_list.append(pack)

    config.set(config_name, pack_list)


def ban(pack_name):
    if pack_name in banned_packs:
        return False
    else:
        banned_packs[pack_name] = True
        save_bans()
        return True


def unban(pack_name):
    if pack_name in banned_packs:
        del banned_packs[pack_name]
        save_bans()
        return True

    return False


def list_packs():
    return list(banned_packs)


def is_banned(pack_name):
    return (pack_name in banned_packs)
