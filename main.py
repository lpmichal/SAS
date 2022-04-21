#!/usr/bin/env python3

import argparse
import sys

def parse():
    # Initiate parser
    parser = argparse.ArgumentParser(description='Encrypts or decrypts a file.')
    subparser = parser.add_subparsers(help="Commands")

    parser_encrypt = subparser.add_parser('encrypt')
    parser_encrypt.add_argument('-i', '--infile', type=argparse.FileType('r', encoding='UTF-8'),
        dest='encrypt', required=True)
    parser_encrypt.add_argument('-o', '--outfile', type=ascii)

    parser_decrypt = subparser.add_parser('decrypt')
    parser_decrypt.add_argument('-i', '--infile', type=argparse.FileType('r', encoding='UTF-8'),
        dest='decrypt', required=True)
    parser_decrypt.add_argument('-o', '--outfile', type=ascii)
    
    args = parser.parse_args()

    if hasattr(args, 'encrypt'):
        encrypt(args.encrypt, args.outfile)
    elif hasattr(args, 'decrypt'):
        decrypt(args.decrypt, args.outfile)
    else:
        sys.exit(1, "Internal Error parsing arguments")

def encrypt(infile, outfile, mode=None):
    print("Encrypt function needs to be implemented")

def decrypt(infile, mode=None, outfile=None):
    print("Decrypt function Needs to be implemented")

def main():
    parse()


if __name__ == '__main__':
    main()