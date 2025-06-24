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


@app.route("/api/files/<fileid>")
def file_content(fileid):

    if not re.match(config.valid_file_id, fileid):
        abort(404)

    for key in get_authorized_keys():
        path = os.path.join(config.data_folder, key, fileid)
        if os.path.exists(path):
            with open(path) as f:
                return Response(f.read(), mimetype="text/plain")

    abort(404)


@app.route("/api/add", methods=["POST"])
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

    return Response(json.dumps({"path": "/api/files/%s" % target_name}), mimetype="application/json")


@app.route("/api/list")
@require_key
def list_content(key):

    key_folder = os.path.join(config.data_folder, key)
    if not os.path.exists(key_folder):
        os.mkdir(key_folder)

    # Ensure consistent URL path for files listed
    # Also, ensure it returns full URLs or paths consistent with API structure
    file_list = []
    for e in os.listdir(key_folder):
        file_list.append({
            "timestamp": os.path.getmtime(os.path.join(key_folder, e)),
            "path": "/api/files/%s" % e
        })
    return Response(json.dumps(file_list), mimetype="application/json")


@app.route("/api/key", methods=["PUT"])
@require_master_key
def add_key():
    new_key = None
    data = request.get_json(silent=True) # Use silent=True to avoid 400 error if no JSON body or wrong Content-Type

    if data and "key" in data:
        key_param = data["key"]
        if not isinstance(key_param, str) or not key_param.strip():
            abort(400, description="Invalid key provided in JSON body.")
        if key_param in get_authorized_keys():
            abort(409, description=f"Key '{key_param}' already exists.") # Conflict if key already exists
        new_key = key_param
    else:
        # Fallback to generating a key if not provided in JSON body or if body is not JSON
        import hashlib
        import time
        while True:
            generated_key = hashlib.md5(str(time.time()).encode()).hexdigest()
            if generated_key not in get_authorized_keys():
                new_key = generated_key
                break

    if new_key is None:
        # This case should ideally not be reached if logic is correct,
        # but as a safeguard:
        abort(500, description="Could not determine key to add.") # Internal server error

    from utils import add_authorized_keys # plural form
    add_authorized_keys(new_key)

    return Response(json.dumps({"key": new_key}), mimetype="application/json"), 201 # 201 Created


@app.route("/api/key/<key>", methods=["DELETE"])
@require_master_key
def remove_key(key):

    if key not in get_authorized_keys():
        abort(404)

    # Use the function from utils.py
    from utils import delete_authorized_keys # plural form
    delete_authorized_keys(key)

    return Response(json.dumps({"status": "deleted", "key": key}), mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0")  # FIXME
