import uuid
import unittest

from common.test_base import TestBase
from module.security import SecurityApi, PRIVATE_KEY, PUBLIC_KEY


class TestSecurityApi(TestBase):

    def setUp(self):
        super().setUp()

    def test_gen_rsa_key_pair(self):
        private_key, public_key = SecurityApi.gen_rsa_key_pair()
        plane_text = b"hello world"
        encrypted_text = SecurityApi.rsa_encrypt(public_key, plane_text)
        decrypted_text = SecurityApi.rsa_decrypt(private_key, encrypted_text)
        self.assertEqual(plane_text, decrypted_text)

    def test_rsa_encrypt(self):
        plane_text = b"hogehoge"
        encrypted_text = SecurityApi.rsa_encrypt(PUBLIC_KEY, plane_text)
        decrypted_text = SecurityApi.rsa_decrypt(PRIVATE_KEY, encrypted_text)
        self.assertEqual(plane_text, decrypted_text)

    def test_rsa_sign(self):
        text = b"fugafuga"
        signature = SecurityApi.rsa_sign(PRIVATE_KEY, text)
        is_valid = SecurityApi.rsa_verify(PUBLIC_KEY, text, signature)
        self.assertTrue(is_valid)
        is_valid = SecurityApi.rsa_verify(PUBLIC_KEY, text + b"hi", signature)
        self.assertFalse(is_valid)

    def test_aes_encrypt(self):
        plane_text = b"piyopiyo"
        aes_key = b"61241C88D6CDB2097EA20577D3A651AC"
        encrypted_text = SecurityApi.aes_encrypt(aes_key, plane_text)
        decrypted_text = SecurityApi.aes_decrypt(aes_key, encrypted_text)
        self.assertEqual(plane_text, decrypted_text)

    def test_authorize(self):
        user_id = str(uuid.uuid4()).encode('utf-8')
        aes_key = b"039D40E223EBE14D5B844FA476786390"
        encrypted_user_id = SecurityApi.rsa_encrypt(PUBLIC_KEY, user_id)
        encrypted_aes_key = SecurityApi.rsa_encrypt(PUBLIC_KEY, aes_key)
        session = self.get_session()
        encrypted_private_key = SecurityApi.authorize(encrypted_user_id, encrypted_aes_key, session)
        session.commit()

    def test_is_valid(self):
        is_valid = SecurityApi.is_valid("request", self.get_session())
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
