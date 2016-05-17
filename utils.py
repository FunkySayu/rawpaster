import hashlib
import time
import os

from functools import wraps
from flask import request, abort

import config


def get_authorized_keys():
    with open(config.authorized_keys_file) as f:
        keys = filter(None, f.readlines())
    return (k.strip() for k in keys)


def add_authorized_keys(key):
    with open(config.authorized_keys_file, "a") as f:
        f.write("%s\n" % key)


def delete_authorized_keys(key):
    keys = get_authorized_keys()

    with open(config.authorized_keys_file, "w") as f:
        f.write("\n".join(k for k in keys if k != key))

def generate_filename(key):
    h = hashlib.md5(("%s%s" % (key, time.time())).encode()).hexdigest()

    while len(h) > config.FILE_ID_LENGTH:
        for k in get_authorized_keys():
            if os.path.exists(os.path.join(config.data_folder, key, h[:config.FILE_ID_LENGTH])):
                break
        else:
            return h[:config.FILE_ID_LENGTH]

        h = h[1:]

    raise ValueError("Unable to create the file !")


def require_key(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.args.get("key") is None:
            abort(401)

        print(get_authorized_keys())
        key = request.args["key"]
        if key not in get_authorized_keys():
            abort(401)

        return func(key, *args, **kwargs)

    return wrapper


def require_master_key(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.args.get("masterkey") is None:
            abort(401)

        if request.arg["masterkey"] != config.master_key:
            abort(401)

        return func(*args, **kwargs)

    return wrapper
