#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any, Callable, Coroutine
from utils import FrozenData
import asyncio
import json
import requests
import warnings
import time as _t


URL = 'https://economia.awesomeapi.com.br/json/all'
LOCAL_FILE = 'data/zxc.json'


def watch(fn: Callable) -> Callable:
    def wrapped(*args: Any, **kwargs: dict) -> Callable:
        start = _t.time()
        result = fn(*args, **kwargs)
        end = _t.time()
        fmt = "function: {}\nexec elapsed time: {}\n"
        print(fmt.format(fn.__name__, (end - start)))
        return result
    return wrapped


@watch
async def _load() -> Coroutine:

    def file_need_updated(file1: Any, file2: Any) -> bool:
        return bool(file1 != file2)

    @watch
    async def create_local_file(data: bytes = None) -> Coroutine:
        msg = 'downloading {}, to JSON'.format(URL, LOCAL_FILE)
        warnings.warn(msg)
        with open(LOCAL_FILE, 'wb') as local:
            local.write(data if data else _get_request(URL))

    if not Path(LOCAL_FILE).exists():
        await create_local_file()

    with open(LOCAL_FILE) as f:
        local_json, latest_data = (json.load(f), _get_request(URL))
        latest_json = json.loads(latest_data)
        if file_need_updated(local_json, latest_json):
            await create_local_file(latest_data)
            return latest_json
        return local_json

@watch
def _get_request(url: str) -> bytes:
    request = requests.get(url)
    return request.content


class Parser:
    def __init__(self) -> None:
        json_data = asyncio.run(_load())
        self._data = dict(json_data)
        self.values = FrozenData(self._data)

    @property
    def data(self) -> str:
        return self._data

    def __str__(self) -> str:
        return f"{json.dumps(self._data, indent=2, sort_keys=True)}"


class Coin:
    def __init__(self, name: str, code: str) -> None:
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return "<Coin({:s}, {:s})>".format(self.name, self.code)


if __name__ == "__main__":
    request = Parser()
