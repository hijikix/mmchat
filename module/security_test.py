import unittest

from common.test_base import TestBase
from module.security import SecurityApi


class TestSecurityApi(TestBase):

    def setUp(self):
        super().setUp()

    def test_encrypt(self):
        plane_text = b"hogehoge"
        encrypted_text = SecurityApi.encrypt(plane_text)
        decrypted_text = SecurityApi.decrypt(encrypted_text)
        self.assertEqual(plane_text, decrypted_text)

    def test_is_valid(self):
        is_valid = SecurityApi.is_valid("request", self.get_session())
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
