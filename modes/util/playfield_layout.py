import os

from ruamel import yaml

class PlayfieldLayout():

    def __init__(self,machine_path):
        # self.config = None
        self.config_file = os.path.join(machine_path, "monitor", "monitor.yaml")
        self.load_config()

    def load_config(self):
        try:
            _yaml = yaml.YAML(typ='safe')
            with open(self.config_file, 'r') as f:
                self.config = _yaml.load(f)
        except FileNotFoundError:
                self.config = dict()
                print (f"!!!!!!!!!!!!!!! Unable to load [{self.config_file}] at runtime")

    def lights(self) -> dict:
        # print (f"!!!!!!!!!!!!! type(self.config['light']) is: {type(self.config['light'])}")
        return self.config["light"]
        #  if not hasattr(self,'config'):
        #       return dict()
        #  elif 'light' not in self.config:
        #       return dict()
        #  else:
        #       return self.config.get("light")
              