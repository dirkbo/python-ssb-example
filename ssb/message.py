import json
import time

from nacl import encoding as nacl_encoding, hash as nacl_hash

from .identity import SsbIdentity
from .database import SsbDatabase


class SSbMessage:
    def __init__(self, ssb_id: SsbIdentity, db: SsbDatabase, content):
        self.identity = ssb_id
        self.key = ""
        self.author = ""
        self.value = ""
        self.create(db, content)

    @staticmethod
    def get_signature(signing_key, unsigned_value):
        unsigned_json = json.dumps(unsigned_value, indent=2)
        unsigned_json_bytes = bytes(unsigned_json, 'utf8')
        signature = signing_key.sign(unsigned_json_bytes).signature
        signature_base64 = nacl_encoding.Base64Encoder.encode(signature).decode()
        return signature_base64 + '.sig.ed25519'

    @staticmethod
    def get_author_id(verify_key):
        key_base64 = verify_key.encode(nacl_encoding.Base64Encoder).decode()
        return '@' + key_base64 + '.ed25519'

    @staticmethod
    def get_message_id(signed_value):
        signed_json = json.dumps(signed_value, indent=2)
        signed_json_bytes = bytes(signed_json, 'utf8')
        hash_base64 = nacl_hash.sha256(
            signed_json_bytes, nacl_encoding.Base64Encoder).decode()
        return '%' + hash_base64 + '.sha256'

    def create(self, db: SsbDatabase, content):
        author = SSbMessage.get_author_id(self.identity.signing_key.verify_key)
        author_state = db.get_previous(author)  # key, sequence

        value = {}
        value['previous'] = author_state[0]
        value['author'] = author
        value['sequence'] = author_state[1] + 1
        value['timestamp'] = round(time.time() * 1000)
        value['hash'] = 'sha256'
        value['content'] = content
        value['signature'] = SSbMessage.get_signature(self.identity.signing_key, value)

        self.key = SSbMessage.get_message_id(value)
        self.value = value
        self.author = author

        db.insert_message(self)

    @property
    def as_dict(self):
        if not self.value:
            return {}

        return {
            "previous": self.value['previous'],
            "author": self.value['author'],
            "sequence": self.value['sequence'],
            "timestamp": self.value['timestamp'],
            "hash": "sha256",
            "content": self.value['content'],
            "signature": self.value['signature']}

    @property
    def json(self):
        return json.dumps(self.as_dict())
