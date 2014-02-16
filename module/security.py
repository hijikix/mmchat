import base64
from datetime import datetime

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from sqlalchemy import Column, String, DateTime

from common.db_base import Base
from settings import PASSPHRASE, PRIVATE_KEY_PATH, PUBLIC_KEY_PATH

PRIVATE_KEY = RSA.importKey(
    open(PRIVATE_KEY_PATH, 'r').read(), passphrase=PASSPHRASE)
PUBLIC_KEY = RSA.importKey(
    open(PUBLIC_KEY_PATH, 'r').read(), passphrase=PASSPHRASE)


class UserAuth(Base):
    __tablename__ = 'user_auth'

    user_id = Column(String(64), primary_key=True)
    aes_key = Column(String(32))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class NotAuthorizedException(Exception):
    pass


class SecurityApi:

    @classmethod
    def gen_rsa_key_pair(cls):
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()
        return private_key, public_key

    @classmethod
    def rsa_encrypt(cls, public_key, text):
        return public_key.encrypt(text, 0)[0]

    @classmethod
    def rsa_decrypt(cls, private_key, encrypted_text):
        return private_key.decrypt(encrypted_text)

    @classmethod
    def rsa_sign(cls, private_key, text):
        return private_key.sign(text, "")

    @classmethod
    def rsa_verify(cls, public_key, text, signature):
        return public_key.verify(text, signature)

    @classmethod
    def _pad(cls, s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (bytes([x]) * x)

    @classmethod
    def aes_encrypt(cls, key, raw):
        padded_raw = cls._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(padded_raw))

    @classmethod
    def _unpad(cls, s):
        return s[:-s[-1]]

    @classmethod
    def aes_decrypt(cls, key, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cls._unpad(cipher.decrypt(enc[16:]))

    @classmethod
    def create_player_auth(cls, player_id, aes_key):
        player_auth = UserAuth.objects.create(
            player_id=player_id, aes_key=aes_key)
        return player_auth

    @classmethod
    def is_valid(cls, request, session):
        print(session.query(UserAuth).all())
        #raise NotAuthorizedException()
        return True
