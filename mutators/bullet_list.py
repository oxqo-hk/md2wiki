import logging
import copy
import re

class Mutator:
    def __init__(self, files, config):
        self.name = "bullet_list"
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
                rex = "^" + "    "*d + "- "
                replace = "*"*(d+1) + " "
                res = re.sub(rex, replace, res, flags=re.M)
        except Exception as e:
            self.logger.error("error in %s: %s", self.name, e)
            return None

        #preventing multi headed list problem like: "* * text"
        try:
            res_sp = res.split("\n")
            for i, line in enumerate(res_sp):
                for d in range(max_depth, 1, -1):
                    if line.startswith("*" * d + " ") and i > 0 and not res_sp[i-1].startswith("*" * (d-1)):
                        line = line.replace("*" * d + " ", ":" * (d-1) + "* ")
                        res_sp[i] = line
        except:
            self.logger.error("error in %s: %s", self.name, e)
            return res
        res = "\n".join(res_sp)
        return res
        
