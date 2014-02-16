import unittest

from common.test_base import TestBase
from module.security import SecurityApi


class TestSecurityApi(TestBase):

    def setUp(self):
        super().setUp()

    def test_rsa_encrypt(self):
        plane_text = b"hogehoge"
        encrypted_text = SecurityApi.rsa_encrypt(plane_text)
        decrypted_text = SecurityApi.rsa_decrypt(encrypted_text)
        self.assertEqual(plane_text, decrypted_text)

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
