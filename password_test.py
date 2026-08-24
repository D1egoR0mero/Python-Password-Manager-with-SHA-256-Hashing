import unittest
import os
import json
from password import (
    generate_password, check_password_strength, hash_password,
    generate_key, initialize_cipher, encrypt_password,
    decrypt_password, add_password, get_password, delete_password
)

class TestPasswordManager(unittest.TestCase):

    def test_generate_password(self):
        password = generate_password()
        self.assertEqual(len(password), 16)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in "!@#$%^&*()_+-=[]|;:,.<>?/" for c in password))

    def test_hash_password_consistency(self):
        pw = "SecurePass123!"
        hash1 = hash_password(pw)
        hash2 = hash_password(pw)
        self.assertEqual(hash1, hash2)

    def test_hash_password_uniqueness(self):
        pw1 = "SecurePass123!"
        pw2 = "DifferentPass456$"
        self.assertNotEqual(hash_password(pw1), hash_password(pw2))

    def test_encryption_decryption(self):
        key = generate_key()
        cipher = initialize_cipher(key)
        password = "MySecurePass!"
        encrypted = encrypt_password(cipher, password)
        decrypted = decrypt_password(cipher, encrypted)
        self.assertEqual(password, decrypted)

    def test_add_and_get_password(self):
        test_website = "example.com"
        test_password = "StrongPassword123!"

        # Clean up file before test
        if os.path.exists("passwords.json"):
            os.remove("passwords.json")

        add_password(test_website, test_password)
        retrieved_password = get_password(test_website)
        self.assertEqual(test_password, retrieved_password)

    def test_delete_password(self):
        test_website = "testdelete.com"
        test_password = "ToDelete123#"

        # Ensure clean state
        if os.path.exists("passwords.json"):
            os.remove("passwords.json")

        add_password(test_website, test_password)
        self.assertEqual(get_password(test_website), test_password)

        delete_password(test_website)
        self.assertIsNone(get_password(test_website))

    def tearDown(self):
        # Clean up test file
        if os.path.exists("passwords.json"):
            os.remove("passwords.json")

if __name__ == '__main__':
    unittest.main()
