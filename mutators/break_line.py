import logging
import re

class Mutator:
    def __init__(self, files, config):
        self.name = "break_line"
        self.files = files
        self.config = config
        self.logger = logging.getLogger()
        self.logger.info("module initiated: " + self.name)

    def do_mutate(self, data):
        self.logger.info("mutating: " + self.name)
        data_sp = data.split("\n")
        in_block=False
        for i, line in enumerate(data_sp):
            skip_line = False
            if len(re.findall("^\s*<source.*>$", line)) > 0:
                #source block start
                in_block=True
            elif len(re.findall("^\s*</source>", line)) > 0:
                skip_line = True
                in_block=False
                #add additional newline to avoid mediawiki source block bug
                data_sp[i] += "\n"
            if len(re.findall("^\s+$", line)) > 0:
                data_sp[i] = ""
            if not (in_block or line.startswith("#") or line.startswith("*") or line.startswith("=") or skip_line):
                data_sp[i] += "</br>" 

        res = "\n".join(data_sp)
        return res