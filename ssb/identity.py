from nacl import signing as nacl_signing


class SsbIdentity:
    def __init__(self):
        self.signing_key = nacl_signing.SigningKey.generate()
