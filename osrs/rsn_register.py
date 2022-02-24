import json
import os

class RsnReg():

    _register_file = 'rsn_registry.json'

    @staticmethod
    def register(discord_name, rsn):
        # Create file if it doesn't exist.
        if not os.path.isfile(RsnReg._register_file):
            f = open(RsnReg._register_file, 'w')
            f.write('{}')
            f.close()

        # Reading, updating and writing JSON data.
        try:
            with open(RsnReg._register_file, 'r+') as f:
                add_reg = {str(discord_name): str(rsn)}
                reg = json.load(f)
                reg.update(add_reg)
            with open(RsnReg._register_file, 'w') as f:
                json.dump(reg, f)
        except:
            return False
        return True


    @staticmethod
    def lookup(discord_name):
        with open(RsnReg._register_file, 'r') as f:
            try:
                reg = json.load(f)
                rsn = reg[str(discord_name)]
                return rsn
            except:
                return None
