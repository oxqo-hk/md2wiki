from ast import Param
import copy
import re
from urllib import parse
import logging
import unicodedata
from bs4 import BeautifulSoup as bs

class Mutator:
    def __init__(self, files, config):
        self.name = "images"
        self.files = files
        self.config = config

    def do_mutate(self, data):
        res = copy.copy(data)
        print(self.files)
        try:
            rex = "!\[.+\]\(.*\)"
            targets = re.findall(rex, data)
            for target in targets:
                rex = "!\[.+\]\((.*)\)"
                key = re.search(rex, target).group(1)
                #key = unicodedata.normalize('NFC', parse.unquote(key))
                print(key)
                if key in self.files:
                    hash_name = self.files[key]
                    replace = "[[File:%s|%dpx]]"%(hash_name, self.config["default_size_pixel"])
                    res = data.replace(target, replace)

        except Exception as e:
            print(e)
            logging.error("error in %s: %s", self.name, e)
            return None
        return res
        