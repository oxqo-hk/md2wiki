import copy
import re
import logging

class Mutator:
    def __init__(self, files, config):
        self.name = "links"
        self.files = files
        self.config = config
        self.logger = logging.getLogger()
        self.logger.info("module initiated: " + self.name)

    def do_mutate(self, data):
        self.logger.info("mutating: " + self.name)
        res = copy.copy(data)
        try:
            rex = "\[(.+?)\]\((.+?)\)"
            found = re.findall(rex, res)
            if len(found) > 0:
                self.logger.info("embedding following links to document:")
                for _, link in found:
                    self.logger.info("\t" + link)
                replace = "[" + r"\2" + " " + r"\1" +"]"
                res = re.sub(rex, replace, res)
        except Exception as e:
            self.logger.error("error in %s: %s, ignoring this mutator", self.name, e)
            return None

        return res
        