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
    def rsa_encrypt(cls, text):
        return PUBLIC_KEY.encrypt(text, 0)[0]

    @classmethod
    def rsa_decrypt(cls, encrypted_text):
        return PRIVATE_KEY.decrypt(encrypted_text)

    @classmethod
    def pad(cls, s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (bytes([x]) * x)

    @classmethod
    def aes_encrypt(cls, key, raw):
        padded_raw = cls.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(padded_raw))

    @classmethod
    def unpad(cls, s):
        return s[:-s[-1]]

    @classmethod
    def aes_decrypt(cls, key, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cls.unpad(cipher.decrypt(enc[16:]))

    @classmethod
    def create_player_auth(cls, player_id, aes_key):
        player_auth = UserAuth.objects.create(
            player_id=player_id, aes_key=aes_key)
        return player_auth

    @classmethod
    def is_valid(cls, request, session):
        print(session.query(UserAuth).all())
        #raise NotAuthorizedException()
        print("testtest")
        return True
