#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from Crypto.Cipher import AES
from Crypto import Random
from argparse import ArgumentParser, FileType
from hashlib import sha512
from getpass import getpass
from tempfile import NamedTemporaryFile
import subprocess as sp
import os
import six
import sys

# Crypto globals
MODE = AES.MODE_CFB
PADDING = b'\x00'

__version__ = '0.2.2'

class EncLengthError(Exception):
    pass

class InvalidPassphrase(Exception):
    pass

def get_args():
    def_file = os.path.join(os.getenv('HOME') or '/', '.pwenc/encrypted')
    pager = os.getenv('PAGER') or 'less'
    editor = os.getenv('EDITOR') or 'vi'

    p = ArgumentParser()
    p.add_argument('-D' , '--debug', action='store_true', default=False,
        help='Turn on debug output [default: %(default)s]')
    p.add_argument('-V' , '--version', action='store_true', default=False,
        help='Print the version and exit [default: %(default)s]')
    sub_p = p.add_subparsers(help='available commands')

    show_sub_p = sub_p.add_parser('show', help='Show the contents of the '
        'encrypted file in your configured PAGER')
    show_sub_p.add_argument('-i', '--infile', type=FileType('rb'),
        default=def_file, help='The file to show [default: %(default)s]')
    show_sub_p.add_argument('-p', '--pager', default=pager,
        help='Override the PAGER you have set in your environment and pipe '
        'the output to a different program [default: %(default)s]')
    show_sub_p.set_defaults(func=show)

    edit_sub_p = sub_p.add_parser('edit', help='Edit the contents of the '
        'encrypted file in your configured EDITOR')
    edit_sub_p.add_argument('-i', '--infile', type=FileType('rb+'),
        default=def_file, help='The file to edit [default: %(default)s]')
    edit_sub_p.add_argument('-e', '--editor', default=editor,
        help='Override the EDITOR you have set in your environment and use '
        'this specified program to edit the file [default: %(default)s]')
    edit_sub_p.set_defaults(func=edit)

    dump_sub_p = sub_p.add_parser('dump', help='Decrypt and dump the '
        'contents of the file to file or stdout')
    dump_sub_p.add_argument('-i', '--infile', type=FileType('rb'),
        default=def_file, help='The file to dump [default: %(default)s]')
    dump_sub_p.add_argument('-o', '--outfile', default='-',
        help='Dump the contents of the encrypted file to this file '
        '[default: STDOUT]')
    dump_sub_p.set_defaults(func=dump)

    enc_sub_p = sub_p.add_parser('enc', help='Encrypt "infile" and output to '
        '"outfile"')
    enc_sub_p.add_argument('-o', '--outfile', default=def_file,
        help='The file to write to [default: %(default)s]')
    enc_sub_p.add_argument('-i' , '--infile', type=FileType('rb'),
        metavar='FILE', default=sys.stdin, help='Encrypt the given file '
        '[default: STDIN]')
    enc_sub_p.set_defaults(func=enc)

    args = p.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    if getattr(args, 'outfile', None):
        if args.outfile == '-':
            args.outfile = sys.stdout
        else:
            _make_dirs(args.outfile)
            args.outfile = open(args.outfile, 'wb')

    return args

#
# Command functions
#
def show(args):
    """
    Decrypt the file and send the output to the specified pager

    args:argparse.Namespace     The cli args
    """
    passphrase = _get_passphrase()
    try:
        # Verify we have a valid password by getting the iterator and reading
        # the first block before opening the pager
        f_iter = _decrypt(passphrase, args.infile)
        block = next(f_iter)
        # Now open the pager and start writing to it
        proc = sp.Popen(args.pager, shell=True, stdin=sp.PIPE, close_fds=True)
        proc.stdin.write(block)
        # Now continue iteration
        for block in f_iter:
            proc.stdin.write(block)
        proc.stdin.close()
        proc.wait()
    finally:
        _close_files(args.infile)


def edit(args):
    """
    Decrypt the file and send the output to the specified pager

    args:argparse.Namespace     The cli args
    """
    passphrase = _get_passphrase()
    tmpfile = NamedTemporaryFile(delete=False)

    # Decrypt the file to a temporary file
    try:
        for block in _decrypt(passphrase, args.infile):
            tmpfile.write(block)
    except Exception as e:
        # If we hit an error here, we want to destroy the tempfile
        tmpfile.close()
        _destroy_tmp(tmpfile.name)
        raise
    
    # Edit the file with the chosen editor
    tmpfile.close()
    proc = sp.Popen('{} {}'.format(args.editor, tmpfile.name), shell=True,
        close_fds=True)
    proc.wait()

    # Now write the new file out encrypted to the specified location
    try:
        with open(tmpfile.name) as fh:
            args.infile.seek(0)
            args.infile.truncate(0)
            for block in _encrypt(passphrase, fh):
                args.infile.write(block)
    except Exception as e:
        print('AN ERROR OCCURRED DURING THE WRITING OF THE ENCRYPTED FILE\n '
            'YOUR UNENCRYPTED FILE IS PRESERVED AT '
            '"{}"!!'.format(tmpfile.name))
        raise
    finally:
        _close_files(args.infile)

    # Finally, destroy the tempfile
    _destroy_tmp(tmpfile.name)


def dump(args):
    """
    Decrypt the given file and dump it to the given file

    args:argparse.Namespace     The cli args
    """
    passphrase = _get_passphrase()
    try:
        for block in _decrypt(passphrase, args.infile):
            args.outfile.write(block)
    finally:
        _close_files(args.infile, args.outfile)


def enc(args):
    """
    Encrypt the given file and dump it to the file location

    args:argparse.Namespace     The cli args
    """
    passphrase = _get_passphrase()
    passphrase2 = _get_passphrase('Enter passphrase again')
    if passphrase != passphrase2:
        raise InvalidPassphrase('Your entered passphrases do not match')

    try:
        for block in _encrypt(passphrase, args.infile):
            args.outfile.write(block)
    finally:
        _close_files(args.outfile, args.infile)


#
# Utility functions
#
def _destroy_tmp(tmp_name):
    """
    Overwrite the tmp file with random bytes, then delete it

    tmp_name:str        The path to the temporary file
    """
    size = os.path.getsize(tmp_name)
    with open(tmp_name, 'rb+') as fh:
        fh.write(os.urandom(size))
    os.unlink(tmp_name)


def _close_files(*files):
    """
    Close any open file handles that are not standard streams

    files:list[file]    The list of file handles to close
    """
    for fh in files:
        if not fh in (sys.stderr, sys.stdout, sys.stdin):
            fh.close()
            os.chmod(fh.name, 0600)


def _get_passphrase(msg='Enter passphrase'):
    """
    Get the passphrase from the user on the command-line

    returns str     Returns the entered passphrase
    """
    return getpass('{}: '.format(msg.rstrip(' :')))
    

def _get_key(key, length=32):
    """
    Pad/truncate the key to length

    key:str     The key to pad out
    length:int  Must be one of {16, 24, 32}
    """
    lengths = (16, 24, 32)
    if not length in lengths:
        raise EncLengthError('Invalid key length {}, must be one '
            'of {}'.format(length, ', '.join(lengths)))

    # Convert to a byte array for encryption usage
    key = key.encode('latin-1')
    key_len = len(key)

    # Pad/truncate if necessary
    if key_len >= length:
        key = key[:length]
    elif key_len < length:
        key = b'{}{}'.format(key, PADDING * (length - key_len))

    return key


def _encrypt(key, fh_to_encrypt):
    """
    Encrypt and yield blocks from the file until the entire file has been
    encrypted

    key:str             The key to use for the encryption
    fh_to_encrypt:file  The file handle to read from

    yields bytes        Yields the encrypted bytes
    """
    key = _get_key(key)
    iv = Random.new().read(AES.block_size)
    salt = Random.new().read(AES.block_size)
    hashed_key = b'{}{}'.format(salt, sha512(b'{}{}'.format(salt, key)).digest())

    aes = AES.new(key, MODE, iv)
    # For the first part, we yield the iv + the encyrpted salted hash
    # (length 70) of the key (for decrypt verification purposes)
    yield b'{}{}'.format(iv, aes.encrypt(hashed_key))
    
    # Now we read by 4k blocks and pad, if necessary, then encrypt and
    # yield chunks
    block = fh_to_encrypt.read(4096)
    while block:
        pad_len = AES.block_size - len(block) % AES.block_size
        if pad_len:
            block = '{}{}'.format(block, PADDING * pad_len)
        yield aes.encrypt(block)
        block = fh_to_encrypt.read(4096)


def _decrypt(key, fh_to_decrypt):
    """
    Decrypt and yield blocks from the file until the entire file has been
    decrypted

    key:str             The key to use for the decryption
    fh_to_decrypt:file  The file handle to read from

    yields bytes        Yields the decrypted bytes
    """
    key = _get_key(key)
    iv = fh_to_decrypt.read(AES.block_size)
    aes = AES.new(key, MODE, iv)
    sha = sha512()
    enc_salt_hash = fh_to_decrypt.read(AES.block_size + sha.digest_size)

    dec_salt_hash = aes.decrypt(enc_salt_hash)
    salt = dec_salt_hash[:AES.block_size]
    hashed_key = dec_salt_hash[AES.block_size:]
    sha.update(b'{}{}'.format(salt, key))

    if sha.digest() != hashed_key:
        raise InvalidPassphrase('The passphrase you entered is not '
            'correct')

    # Now, on to the decryption
    block = fh_to_decrypt.read(4096)
    while block:
        yield aes.decrypt(block).rstrip(PADDING)
        block = fh_to_decrypt.read(4096)


def _make_dirs(fname):
    """
    Create intermediate directories, if necessary, for file storage

    fname:str       The cli args
    """
    dirname = os.path.dirname(fname)
    if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname, 0700)


#
# Main entry point
#
def main():
    args = get_args()

    # Call the command function
    try:
        args.func(args)
    except InvalidPassphrase as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.debug:
            import traceback
            exc = traceback.format_exc()
            print(exc, file=sys.stderr)
        print('An unknown error has occurred: {}'.format(e), file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
