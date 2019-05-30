#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import json
import requests
import warnings

URL = 'https://economia.awesomeapi.com.br/json/all'
LOCAL_JSON = 'data/zxc.json'

def _load():
    if not Path(LOCAL_JSON).exists():
        msg = 'downloading {}, to JSON'.format(URL, LOCAL_JSON)
        warnings.warn(msg)
        with open(LOCAL_JSON, 'wb') as local:
            local.write(_get_request(URL))

    with open(LOCAL_JSON) as json_file:
        return json.load(json_file)


def _get_request(url: str) -> bytes:
    request = requests.get(url)
    return request.content


class Parser:
    def __init__(self, url:str):
        self.data = json.loads(_get_request(url))

    def __repr__(self):
        return "Parser({})".format(self.data)

    def __str__(self):
        return f"{json.dumps(self.data, indent=2, sort_keys=True)}"


class Coin:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    def __repr__(self):
        return "Coin({:s}, {:s})".format(self.name, self.code)


if __name__ == "__main__":
    request = Parser('https://economia.awesomeapi.com.br/json/all')

