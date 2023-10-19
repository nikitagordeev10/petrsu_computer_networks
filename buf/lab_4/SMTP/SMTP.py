# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (1) Подключение к серверу ^^^^^^^^^^^^^^^^^^^^^^^^^^^
from socket import *

msg = "\r\n Я люблю компьютерные сети!"
endmsg = "\r\n.\r\n"

mailServer  = 'mail.cs.karelia.ru' # выбираем почтовый сервер 
mailPort = 25

clientSocket = socket(AF_INET, SOCK_STREAM) # создаем сокет IPv4, TCP
clientSocket.connect((mailServer , mailPort)) # устанавливаем TCP-соединение

recv = clientSocket.recv(1024)
print(recv) # выводим ответ сервера
if int(recv[:3]) != int('220'):
    print('код 220 от сервера не получен.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (2) Проверка подлинности и приветствия ^^^^^^^^^^^^^^^^^^^^^^^^^^^
heloCommand = 'HELO  gordeev@kappa.cs.petrsu.ru\r\n'
clientSocket.send(heloCommand.encode()) # отправляем команду HELLO

recv1 = clientSocket.recv(1024)
print(recv1) # выводим ответ сервера
if int(recv1[:3]) != int('250'):
    print('код 250 от сервера не получен.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (3) Установление отправителя ^^^^^^^^^^^^^^^^^^^^^^^^^^^
mailFromCommand = 'MAIL FROM: <gordeev@cs.petrsu.ru>\r\n'
clientSocket.send(mailFromCommand.encode()) # отправляем команду MAIL FROM

recv2 = clientSocket.recv(1024)
print(recv2) # выводим ответ сервера
if int(recv2[:3]) != int('250'):
    print('код 250 от сервера не получен.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (4) Установление получателей ^^^^^^^^^^^^^^^^^^^^^^^^^^^
rcptToCommand = 'RCPT TO: <gordeev@cs.petrsu.ru>\r\n'
clientSocket.send(rcptToCommand.encode())# отправляем команду RCPT TO

recv3 = clientSocket.recv(1024)
print(recv3) # выводим ответ сервера

if int(recv3[:3]) != int('250'):
    print('код 250 от сервера не получен.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (5) Отправка письма ^^^^^^^^^^^^^^^^^^^^^^^^^^^
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode()) # отправляем команду DATA 
 
recv4 = clientSocket.recv(1024)
print(recv4) # выводим ответ сервера
if int(recv4[:3]) != int('354'):
    print('код 354 от сервера не получен.')

clientSocket.send('From: Отправитель Никита Гордеев <gordeev@cs.petrsu.ru>\r\n'.encode()) # отправляем данные сообщения.
clientSocket.send('To: Получатель Никита Гордеев <gordeev@cs.petrsu.ru>\r\n'.encode())
clientSocket.send('Subject: Компьютерные сети, лабораторая 4, часть 1\r\n'.encode())
clientSocket.send('Content-Type: text/plain; charset=utf-8\r\n'.encode())
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())# Сообщение завершается одинарной точкой.

recv5 = clientSocket.recv(1024)
print(recv5)
if int(recv5[:3]) != int('250'):
    print('код 250 от сервера не получен.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (6) Закрытие соединения ^^^^^^^^^^^^^^^^^^^^^^^^^^^
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode()) # отправляем команду QUIT
recv6 = clientSocket.recv(1024)

print(recv6) # получаем ответ сервера
if int(recv6[:3]) != int('221'):
    print (recv6[:3])
    print('код 221 от сервера не получен.')

clientSocket.close() # закрываем соединение
