import json
from nacl import signing as nacl_signing


class SsbIdentity:
    def __init__(self, id_file="identity.json"):
        self.signing_key = ""
        self.load_identity(id_file=id_file)

    def create_new_identity(self, id_file="identity.json"):
        self.signing_key = nacl_signing.SigningKey.generate()
        self.save_identity(id_file=id_file)

    def load_identity(self, id_file="identity.json", create_if_not_exists: bool = True):
        try:
            with open(id_file) as jsonIdFile:
                json_object = json.load(jsonIdFile)
                seed = json_object["seed"].encode('latin-1')
                self.signing_key = nacl_signing.SigningKey(seed=seed)
        except FileNotFoundError:
            if create_if_not_exists:
                self.create_new_identity(id_file=id_file)

    def save_identity(self, id_file="identity.json"):
        with open(id_file, 'w') as jsonFile:
            json.dump(self.dict, jsonFile)
            jsonFile.close()

    @property
    def dict(self):
        return {'seed': self.signing_key.__dict__['_seed'].decode('latin-1')}

