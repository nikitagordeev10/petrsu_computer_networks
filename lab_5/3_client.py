from socket import *
import sys

# проверка корректности передачи аргументов из командной строки
if len(sys.argv) != 4:
    print("Запуск: python3 3_client.py localhost 8080 site_1.html")
    sys.exit(1)

server_host = sys.argv[1]  # IP-адрес или имя сервера
server_port = int(sys.argv[2])  # порт сервера
file_name = sys.argv[3]  # полный путь хранения файла на сервере

# Создаем клиентский сокет TCP и устанавливаем соединение с сервером
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server_host, server_port))

# Формируем HTTP-запрос методом GET
http_request = f"GET /{file_name} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"

# Отправляем HTTP-запрос серверу
clientSocket.send(http_request.encode())

# Получаем ответ сервера
response = b""
while True:
    data = clientSocket.recv(4096)
    if not data:
        break
    response += data

# Отображаем ответ сервера
print(response.decode())

# Закрываем клиентский сокет
clientSocket.close()