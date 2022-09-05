import copy
import re
import logging

class Mutator:
    def __init__(self, files, config):
        self.name = "source_code"
        self.files = files
        self.config = config
        self.logger = logging.getLogger()
        self.logger.info("module initiated: " + self.name)

    def do_mutate(self, data):
        self.logger.info("mutating: " + self.name)
        res = copy.copy(data)
        use_correction = False
        if self.config is not None and "use_correction" in self.config and self.config["use_correction"]:
            for key in self.config["corrections"]:
                val = self.config["corrections"][key]
                res = res.replace("\n```" + key, "\n```" + val)
        
        try:
            rex = "^\s*```([^\s]+)\n"
            replace = '<source lang="' + r"\1" + '">\n'
            res = re.sub(rex, replace, res, flags=re.M)
            rex = "^\s*```"
            replace = "</source>"
            res = re.sub(rex, replace, res, flags=re.M)
        except Exception as e:
            self.logger.error("error in %s: %s, ignoring this mutator", self.name, e)
            return None

        return res
        