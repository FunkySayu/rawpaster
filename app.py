#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import logging
import json

from flask import Flask, request, abort, Response
from utils import generate_filename, require_key, get_authorized_keys, require_master_key
import config


app = Flask(__name__)
app.secret_key = os.urandom(128)


@app.route("/")
def index():

    try:
        with open(config.index_page) as f:
            data = f.read()
    except FileNotFoundError:
        data = "<html><head></head><body><h1>Index file not found !</h1></body></html>"

    return data


@app.route("/<fileid>")
def file_content(fileid):

    if not re.match(config.valid_file_id, fileid):
        abort(404)

    for key in get_authorized_keys():
        path = os.path.join(config.data_folder, key, fileid)
        if os.path.exists(path):
            with open(path) as f:
                return Response(f.read(), mimetype="text/plain")

    abort(404)


@app.route("/add", methods=["POST"])
@require_key
def add_content(key):

    key_folder = os.path.join(config.data_folder, key)
    if not os.path.exists(key_folder):
        logging.info("Folder %s does not exists ; creating.", key_folder)
        os.mkdir(key_folder)

    target_name = generate_filename(key)
    with open(os.path.join(key_folder, target_name), "w") as f:
        logging.info("User identified by key '%s' has pushed a file.", key)
        f.write(request.data.decode())

    return "/%s" % target_name


@app.route("/list")
@require_key
def list_content(key):

    key_folder = os.path.join(config.data_folder, key)
    if not os.path.exists(key_folder):
        os.mkdir(key_folder)

    return json.dumps([(os.path.getmtime(os.path.join(key_folder, e)), "/%s" % e)
                      for e in os.listdir(key_folder)])


@app.route("/key", methods=["PUT"])
@require_master_key
def add_key():

    if "key" in requests.params:
        key = requests.params["key"]
        if key in get_authorized_keys():
            abort(409)
    else:
        while True:
            key = hashlib.md5(str(time.time()).encode())
            if key not in get_authorized_keys():
                break

    add_authorized_key(key)
    return key


@app.route("/key/<key>", methods=["DELETE"])
@require_master_key
def remove_key(key):

    if key not in get_authorized_keys():
        abort(404)

    delete_authorized_key(key)
    return key


if __name__ == "__main__":
    app.run(host="0.0.0.0")  # FIXME
