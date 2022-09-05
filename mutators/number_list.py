import copy
import re
import logging

class Mutator:
    def __init__(self, files, config):
        self.name = "number_list"
        self.files = files
        self.config = config
        self.logger = logging.getLogger()
        self.logger.info("module initiated: " + self.name)
        
    def do_mutate(self, data):
        self.logger.info("mutating: " + self.name)
        res = copy.copy(data)
        max_depth=5 #default
        if self.config is not None and "max_depth" in self.config:
            max_depth = self.config["max_depth"]
        self.logger.info("using max depth: %d"%max_depth)
        try:
            for d in range(max_depth, -1, -1):
                rex = "^" + "    "*d + "[0-9]\. "
                replace = "#"*(d+1) + " "
                res = re.sub(rex, replace, res, flags=re.M)
        except Exception as e:
            self.logger.error("error in %s: %s", self.name, e)
            return None
        return res
        
