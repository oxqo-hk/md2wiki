#[[Category:클라우드개발팀|클라우드개발팀]]
import logging
import copy

class Mutator:
    def __init__(self, files, config):
        self.name = "category"
        self.files = files
        self.config = config
        self.logger = logging.getLogger()
        self.logger.info("module initiated: " + self.name)

    def do_mutate(self, data):
        self.logger.info("mutating: " + self.name)
        if self.config == None:
            return data
        res = copy.copy(data)
        for category in self.config:
            self.logger.info("adding category: %s"%category)
            res += "\n" + category
        return res
