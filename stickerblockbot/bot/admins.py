from . import config

config_name = "admins"
admins = {}
owner = ""


def init():
    global admins
    global owner
    admin_list = config.get(config_name)
    if admin_list is None or type(admin_list).__name__ != "list":
        admins = {}
    else:
        for admin in admin_list:
            admins[admin] = True

    config_owner = config.get("owner")
    if config_owner is None or type(config_owner).__name__ != "str":
        owner = ""
    else:
        owner = config_owner.lower()


def save_admins():
    admin_list = []
    for admin in admins.keys():
        admin_list.append(admin)

    config.set(config_name, admin_list)


def add(username):
    if username.lower() in admins:
        return False

    admins[username.lower()] = True
    save_admins()
    return True


def remove(username):
    if username.lower() in admins:
        del admins[username.lower()]
        save_admins()
        return True

    return False


def list_admins():
    admin_list = list(admins)
    admin_list.append(owner)
    return sorted(admin_list)


def is_admin(username):
    return (username.lower() in admins or username.lower() == owner)


def is_owner(username):
    return (username.lower() == owner)
