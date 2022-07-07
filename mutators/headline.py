import copy
import re
import logging

class Mutator:
    def __init__(self, files, config):
        self.name = "headline"
        self.files = files
        self.config = config
        self.logger = logging.getLogger()
        self.logger.info("module initiated: " + self.name)

    def do_mutate(self, data):
        self.logger.info("mutating: " + self.name)
        res = copy.copy(data)
        try:
            for n in range(1, 4):
                rex = "\n" + "#"*n + " (.*)\n"
                replace = "\n" + "="*n + r"\1" + "="*n
                res = re.sub(rex, replace, res)
        except Exception as e:
            self.logger.error("error in %s: %s", self.name, e)
            return None
        return res
        