import main
import sys
import os
from io import StringIO
from contextlib import redirect_stdout
import unittest
from unittest.mock import patch

class TestMain(unittest.TestCase):
    '''
    Tests the main program's functionality
    '''

    def test_cli_error(self):
        '''
        Test help message displays with no arguments specified
        '''
        args = ['main']
        with patch.object(sys, 'argv', args):
            out = StringIO()
            with redirect_stdout(out):
                with self.assertRaises(SystemExit) as error:
                    main.parse()
                    self.assertEquals(0, error.exception.code) # Successful exit
            stdout = out.getvalue()
        self.assertTrue('usage: main [-h] {encrypt,decrypt} ...' in stdout)
        self.assertTrue('Encrypts or decrypts a file.' in stdout)

    @patch('main.encrypt')
    def test_cli_encrypt(self, mock):
        '''
        Test arguments are read in and encrypt function is called
        '''
        args = ['main', 'encrypt', 'test_file.txt']
        with patch.object(sys, 'argv', args):
            main.parse()
        self.assertTrue(mock.called)

    @patch('main.decrypt')
    def test_cli_decrypt(self, mock):
        '''
        Test arguments are read in and decrypt function is called
        '''
        args = ['main', 'decrypt', 'test_file.txt', '-k', 'fake.key']
        with patch.object(sys, 'argv', args):
            main.parse()
        self.assertTrue(mock.called)

    def test_encrypt_decrypt(self):
        '''
        Tests the encryption and decryption functions work as intended
        '''
        with open('test_file.txt', 'r') as handle:
            original = handle.read()
    
        # Test default encryption/decryption
        main.encrypt('test_file.txt', None)

        with open('test_file.txt', 'r') as handle:
            result = handle.read()

        self.assertNotEqual(original, result)
        self.assertTrue(os.path.exists('test_file.txt.key'))

        main.decrypt('test_file.txt', None, 'test_file.txt.key')

        with open('test_file.txt', 'r') as handle:
            result = handle.read()

        self.assertEqual(original, result)
        self.assertTrue(not os.path.exists('test_file.txt.key'))

        # Test encryption/decryption with specified outfile
        main.encrypt('test_file.txt', 'encrypted_file')

        with open('encrypted_file', 'r') as handle:
            result = handle.read()

        self.assertNotEqual(original, result)
        self.assertTrue(os.path.exists('encrypted_file.key'))

        main.decrypt('encrypted_file', 'decrypted_file.txt', 'encrypted_file.key')

        with open('decrypted_file.txt', 'r') as handle:
            result = handle.read()

        self.assertEqual(original, result)
        self.assertTrue(not os.path.exists('encrypted_file.key'))

        # clean up files
        os.remove('encrypted_file')
        os.remove('decrypted_file.txt')

if __name__ == '__main__':
    unittest.main()