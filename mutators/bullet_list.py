import logging
import copy
import re

class Mutator:
    def __init__(self, files, config):
        self.name = "bullet_list"
        self.files = files
        self.config = config

    def do_mutate(self, data):
        res = copy.copy(data)
        max_depth=5 #default
        if self.config is not None and "max_depth" in self.config:
            max_depth = self.config["max_depth"]
        try:
            for d in range(max_depth, -1, -1):
                rex = "\n" + "    "*d + "- "
                replace = "\n" + "*"*(d+1) + " "
                res = re.sub(rex, replace, res)
        except Exception as e:
            logging.error("error in %s: %s", self.name, e)
            return None
        return res
        
