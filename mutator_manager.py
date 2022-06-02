import json
import logging
import importlib

class Mutator_manager:
    def __init__(self, config_file, data_files):
        self._config = {}
        self.files = data_files
        self.mutator_list = {}
        self._parse_config(config_file)
        self._get_mutator_set()
        
    def _parse_config(self, config_file):
        data = {}
        try:
            with open(config_file) as f:
                data = json.load(f)
        except Exception as e:
            logging.error("parsing json config failed", e)
            raise e
        self._config = data
    def _get_mutator_set(self):
        for mut_name in self._config['mutators']:
            mod=None
            try: 
                mod=importlib.import_module("mutators." + mut_name, mut_name)
            except Exception as e:
                print(e)
                logging.warning("ignoring unrecognized mutator: %s"%mut_name)
                continue
            if mut_name in self._config['extra_options']:
                config = self._config['extra_options'][mut_name]
            else:
                config =  None
            
            mutator = mod.Mutator(self.files, config)
            self.mutator_list[mut_name] = mutator
            
    def mutate_all(self, data):
        for key in self.mutator_list:
            mutator = self.mutator_list[key]
            res = mutator.do_mutate(data)
            if res == None:
                logging.error("error in mutator: %s", key)
            else:
                data = res
        
        return data

