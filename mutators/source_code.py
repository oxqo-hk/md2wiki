import copy
import re
import logging

class Mutator:
    def __init__(self, files, config):
        self.name = "source_code"
        self.files = files
        self.config = config


    def do_mutate(self, data):
        res = copy.copy(data)
        max_depth=5 #default
        use_correction = False
        if self.config is not None and "use_correction" in self.config:
            use_correction = self.config["use_correction"]
        
        try:
            rex = "\n```([^\s]+)\n"
            lang = re.search(rex, res).group(1)
            if use_correction and lang in self.config["known_language_correction"]:
                lang = self.config["known_language_correction"][lang]
            replace = '\n<source lang="%s">\n'%lang
            res = re.sub(rex, replace, res)
            rex = "\n```"
            replace = "\n</source>"
            res = re.sub(rex, replace, res)
        except Exception as e:
            logging.error("error in %s: %s, ignoring this mutator", self.name, e)
            return None

        return res
        