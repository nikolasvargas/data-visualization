#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

def _get_request(url: str) -> dict:
    request = requests.get(url)
    data = json.loads(request.content)
    return data

class Parser:
    def __init__(self, url:str):
        self.data = _get_request(url)

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
    c = Coin(request.data['USD']['name'], request.data['USD']['code'])

    for k in request.data:
        print("{} -> {}".format(k, request.data[k]))
