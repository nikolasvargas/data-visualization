#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import abc
from pathlib import Path
from typing import Any
import json
import requests
import warnings

URL = 'https://economia.awesomeapi.com.br/json/all'
LOCAL_JSON = 'data/zxc.json'

def __load() -> dict:
    if not Path(LOCAL_JSON).exists():
        msg = 'downloading {}, to JSON'.format(URL, LOCAL_JSON)
        warnings.warn(msg)
        with open(LOCAL_JSON, 'wb') as local:
            local.write(get_request(URL))

    with open(LOCAL_JSON) as json_file:
        return json.load(json_file)


def get_request(url: str) -> bytes:
    request = requests.get(url)
    return request.content


class Ojson:
    """
    criado apenas para ler atributos de objetos do tipo dict ou JSON
    usando notação de atributos
    """
    def __init__(self, mapping) -> None:
        self.__data = dict(mapping)

    def __getattr__(self, name: Any) -> Any:
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return Ojson.build(self.__data[name])

    @classmethod
    def build(cls, obj: Any) -> Any:
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


class Parser:
    def __init__(self, url: str) -> None:
        json_data = json.loads(get_request(url))
        self.__data = dict(json_data)

    def __repr__(self) -> str:
        return "Parser({})".format(self.__data)

    def __str__(self) -> str:
        return f"{json.dumps(self.__data, indent=2, sort_keys=True)}"


class Coin:
    def __init__(self, name: str, code: str) -> None:
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return "Coin({:s}, {:s})".format(self.name, self.code)


if __name__ == "__main__":
    request = Parser('https://economia.awesomeapi.com.br/json/all')

