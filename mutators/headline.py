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
                self.logger.info("%d"%n)
                rex = "^" + "#"*n + " (.*)\n"
                self.logger.info(re.findall(rex, res, flags=re.M))
                replace = "="*n + r"\1" + "="*n + "\n"
                res = re.sub(rex, replace, res, flags=re.M)
        except Exception as e:
            self.logger.error("error in %s: %s", self.name, e)
            return None
        return res
        