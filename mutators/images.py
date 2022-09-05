import copy
import re
from urllib import parse
import logging

class Mutator:
    def __init__(self, files, config):
        self.name = "images"
        self.files = files
        self.config = config
        self.logger = logging.getLogger()
        self.logger.info("module initiated: " + self.name)

    def do_mutate(self, data):
        self.logger.info("mutating: " + self.name)
        res = copy.copy(data)
        self.logger.info("embedding following images:")
        self.logger.info(self.files)
        try:
            rex = "!\[.+\]\(.*\)"
            targets = re.findall(rex, data)
            if len(targets) > 0:
                self.logger.info("Converting following texts:")
                self.logger.info(targets)
                self.logger.info("Changing file names into:")
            for target in targets:
                rex = "!\[.+\]\((.*)\)"
                key = re.search(rex, target).group(1)
                #key = unicodedata.normalize('NFC', parse.unquote(key))
                if key in self.files:
                    hash_name = self.files[key]
                    replace = "[[File:%s|%dpx]]"%(hash_name, self.config["default_size_pixel"])
                    self.logger.info(parse.unquote(target) + " -> " + replace)
                    res = res.replace(target, replace)

        except Exception as e:
            print(e)
            self.logger.error("error in %s: %s", self.name, e)
            return None
        return res
        