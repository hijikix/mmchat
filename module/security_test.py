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
        self.assertTrue(is_valid)

    def test_aes_encrypt(self):
        plane_text = b"piyopiyo"
        key = b"61241C88D6CDB2097EA20577D3A651AC"
        encrypted_text = SecurityApi.aes_encrypt(key, plane_text)
        decrypted_text = SecurityApi.aes_decrypt(key, encrypted_text)
        self.assertEqual(plane_text, decrypted_text)

    def test_is_valid(self):
        is_valid = SecurityApi.is_valid("request", self.get_session())
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
