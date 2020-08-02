#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Config:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r', encoding='utf-8') as wfile:
            self.data = json.load(wfile)

    def get_value_by_1key(self, key):
        return self.data[key]

    def get_value_by_2key(self, key1, key2):
        return self.data[key1][key2]

    def get_value_by_3key(self, key1, key2, key3):
        return self.data[key1][key2][key3]

    def get_value_by_4key(self, key1, key2, key3, key4):
        return self.data[key1][key2][key3][key4]

config = Config()
