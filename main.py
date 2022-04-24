#!/usr/bin/env python3

import argparse
import sys
import os
from cryptography.fernet import Fernet

# To do: Figure out how to validate users' filepaths

def get_filename(filepath):
    '''
    Gets the filename of the filepath
    '''
    split_path =  filepath.split('/')
    return split_path.pop()

def encrypt(infile, outfile):
    '''
    Encrypts the specified input file and writes the encrypted file
    and encryption key to the working directory

    Parameters:
        infile: The filepath to encrypt
        outfile: The filepath to where the output will be placed
    '''
    key = Fernet.generate_key()
    f = Fernet(key)

    if outfile is None:
        outfile = get_filename(infile)

    with open(infile, 'rb') as handle:
        data = handle.read()

    with open(outfile + '.key', 'wb') as handle:
        handle.write(key)

    encrypted_data = f.encrypt(data)

    with open(outfile, 'wb') as handle:
        handle.write(encrypted_data)

def decrypt(infile, outfile, key):
    '''
    Decrypts the specified infile and outputs the result to an outfile
    using the encryption key

    Parameters:
        infile: The filepath to decrypt
        outfile: The filepath to where the output will be placed
        key: The filepath of the encryption key
    '''
    with open(key, 'rb') as handle:
        encryption_key = handle.read()

    f = Fernet(encryption_key)

    with open(infile, 'rb') as handle:
        encrypted_file = handle.read()

    decrypted_data = f.decrypt(encrypted_file)

    if outfile is None:
        outfile = get_filename(infile)
    
    with open(outfile, 'wb') as handle:
        handle.write(decrypted_data)

    # Remove key if possible
    try:
        os.remove(key)
    except OSError:
        pass


def parse():
    '''
    Creates a CLI interface and processes passed in arguments
    '''
    parser = argparse.ArgumentParser(description='Encrypts or decrypts a file.')

    subparser = parser.add_subparsers()

    parser_encrypt = subparser.add_parser('encrypt')
    parser_encrypt.add_argument('original_file', type=str,
        help='The file to be encrypted')
    parser_encrypt.add_argument('-o', '--outfile', type=str)

    parser_decrypt = subparser.add_parser('decrypt')
    parser_decrypt.add_argument('encrypted_file', type=str,
        help='The file to be decrypted')
    parser_decrypt.add_argument('-k', '--key', type=str,
        dest='key', required=True)
    parser_decrypt.add_argument('-o', '--outfile', type=str)
    
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if hasattr(args, 'original_file'):
        encrypt(args.original_file, args.outfile)
    elif hasattr(args, 'encrypted_file'):
        decrypt(args.encrypted_file, args.outfile, args.key)
    else:
        print('Error parsing arguments')
        sys.exit(1)


if __name__ == '__main__':
    parse()