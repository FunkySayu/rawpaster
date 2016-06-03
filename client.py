#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os
import optparse
import time
import requests


default_host = os.environ.get("RAWPASTER_CLIENT_HOST")
default_key = os.environ.get("RAWPASTER_CLIENT_KEY")


def send(data, host=default_host, key=default_key):
    if host is None:
        raise ValueError("A non None host is required.")
    if key is None:
        raise ValueError("A non None key is required.")

    answer = requests.post("%s/add" % host, params=dict(key=key), data=data)
    return "%s%s" % (host, answer.text)


def list_uploaded(host=default_host, key=default_key):
    if host is None:
        raise ValueError("A non None host is required.")
    if key is None:
        raise ValueError("A non None key is required.")

    answer = requests.get("%s/list" % host, params=dict(key=key))
    return [(time, "%s%s" % (host, addr)) for (time, addr) in json.loads(answer.text)]


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option(
            "-H",
            "--host",
            dest="host",
            help=("Hostname to reach (can also be put in the"
                " environment variable 'RAWPASTER_CLIENT_HOST')."
                " Example: 'http://foobar.com'"))
    parser.add_option(
            "-k",
            "--key",
            dest="key",
            help=("Key token to upload data (can also be put in the"
                " environment variable 'RAWPASTER_CLIENT_KEY')"))
    parser.add_option(
            "-L",
            "--list",
            dest="list",
            default=False,
            action="store_true",
            help="List elements uploaded.")

    opts, args = parser.parse_args()

    host = opts.host if opts.host is not None else default_host
    key = opts.key if opts.key is not None else default_key

    if opts.list:
        uploaded = sorted(list_uploaded(host, key), key=lambda x: x[0], reverse=True)

        if uploaded:
            print("Uploaded elements :")
            print("\n".join(" - %-30s %s" % (time.ctime(date), addr)
                for date, addr in uploaded))
        else:
            print("No elements uploaded.")
    else:
        print(send(sys.stdin.read(), host, key))
