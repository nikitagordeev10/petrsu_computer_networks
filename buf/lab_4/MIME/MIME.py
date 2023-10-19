# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (0) Внутренняя подготовка ^^^^^^^^^^^^^^^^^^^^^^^^^^^
import ssl
from socket import *
import base64
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
from CREDENTIALS import gmail_username, gmail_password

image_path = 'petrsu.jpeg'

msg = MIMEMultipart()
endmsg = "\r\n.\r\n"

text = MIMEText("Я люблю компьютерные сети!", _charset="utf-8")
msg.attach(text)

if os.path.exists(image_path):
    with open(image_path, "rb") as img:
        image = MIMEImage(img.read())
        image.add_header("Content-Disposition", "attachment", filename=image_path) 
        msg.attach(image)

email_message = msg.as_string()

mailServer  = 'smtp.gmail.com'
mailPort = 587

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (1) Подключение к серверу ^^^^^^^^^^^^^^^^^^^^^^^^^^^
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))
recv = clientSocket.recv(1024) # сервер приветствует вас и готов начать общение
print(recv)
if int(recv[:3]) != 220:
    print('код 220 от сервера не получен.') 

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (2) Проверка подлинности и приветствия ^^^^^^^^^^^^^^^^^^^^^^^^^^^
heloCommand = 'HELO smtp.gmail.com\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024) # сервер подтверждает команду HELO
print(recv1)
if int(recv1[:3]) != 250:
    print('код 250 от сервера не получен.')

# START TLS command
starttls_command = "STARTTLS\r\n"
clientSocket.send(starttls_command.encode())
recv2 = clientSocket.recv(1024) # сервер подтверждает готовность перейти на TLS
print(recv2)
if int(recv2[:3]) != 220:
    print('код 220 от сервера не получен для STARTTLS.')

# метод wrap_socket() для обновления сокета клиента в режиме TLS/SSL.
clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

# Аутентификация
auth_command = "AUTH LOGIN\r\n"
clientSocket.send(auth_command.encode())
recv3 = clientSocket.recv(1024)  
print(recv3) # сервер просит предоставить имя пользователя (логин)
if int(recv3[:3]) != 334:
    print('код 334 от сервера не получен для AUTH LOGIN.')

# Отправка имени пользователя
clientSocket.send(base64.b64encode(gmail_username.encode()) + b"\r\n")
recv4 = clientSocket.recv(1024) 
print(recv4) # сервер просит предоставить пароль
if int(recv4[:3]) != 334:
    print('код 334 от сервера не получен для USERNAME.')

# Отправка пароля
clientSocket.send(base64.b64encode(gmail_password.encode()) + b"\r\n")
recv5 = clientSocket.recv(1024) 
print(recv5) # сервер принимает учетные данные и разрешает доступ к отправке писем
if int(recv5[:3]) != 235:
    print('код 235 от сервера не получен для PASSWORD.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (3) Установление отправителя ^^^^^^^^^^^^^^^^^^^^^^^^^^^
mailFromCommand = 'MAIL FROM: <{}>\r\n'.format(gmail_username)
clientSocket.send(mailFromCommand.encode())
recv6 = clientSocket.recv(1024)
print(recv6)
if int(recv6[:3]) != 250:
    print('код 250 от сервера не получен после MAIL FROM.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (4) Установление получателей ^^^^^^^^^^^^^^^^^^^^^^^^^^^
toEmail = '<nikitagordeev10@yandex.ru>'

rcptToCommand = 'RCPT TO: {}\r\n'.format(toEmail)
clientSocket.send(rcptToCommand.encode())
recv7 = clientSocket.recv(1024)
print(recv7)
if int(recv7[:3]) != 250:
    print('код 250 от сервера не получен после RCPT TO.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (5) Отправка письма ^^^^^^^^^^^^^^^^^^^^^^^^^^^
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode()) # отправляем команду DATA  
recv8 = clientSocket.recv(1024)
print(recv8)
if int(recv8[:3]) != 354:
    print('код 354 от сервера не получен после DATA.')
clientSocket.send('From: Отправитель {} <{}>\r\n'.format("ОТ НИКИТЫ ГОРДЕЕВА", gmail_username).encode())
clientSocket.send('To: Получатель {} <{}>\r\n'.format("ДЛЯ НИКИТЫ ГОРДЕЕВА", toEmail).encode())
clientSocket.send('Subject: Компьютерные сети, лабораторая 4, часть 1\r\n'.encode())
clientSocket.send('Content-Type: text/plain; charset=utf-8\r\n'.encode())
clientSocket.send(email_message.encode())
clientSocket.send(endmsg.encode())
recv9 = clientSocket.recv(1024)
print(recv9)
if int(recv9[:3]) != 250:
    print('код 250 от сервера не получен после отправки сообщения.')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ (6) Закрытие соединения ^^^^^^^^^^^^^^^^^^^^^^^^^^^
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode()) # отправляем команду QUIT
recv10 = clientSocket.recv(1024) # получаем ответ сервера
print(recv10)
if int(recv10[:3]) != 221:
    print('код 221 от сервера не получен.')

clientSocket.close() # закрываем соединение
