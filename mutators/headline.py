import copy
import re
import logging
from urllib import parse

class Mutator:
    def __init__(self, files, config):
        self.name = "headline"
        self.files = files
        self.config = config


    def do_mutate(self, data):
        res = copy.copy(data)
        try:
            for n in range(1, 4):
                rex = "\n" + "#"*n + " (.*)\n"
                replace = "\n" + "="*n + r"\1" + "="*n
                res = re.sub(rex, replace, res)
        except Exception as e:
            logging.error("error in %s: %s", self.name, e)
            return None
        return res
        