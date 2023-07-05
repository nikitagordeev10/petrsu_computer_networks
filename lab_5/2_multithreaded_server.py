from socket import *
import threading

def handle_client(connectionSocket):
    # Обрабатываем запрос клиента
    try:
        # Получаем сообщение от клиента
        message = connectionSocket.recv(1024)

        # Выделяем имя файла из запроса
        filename = message.split()[1]

        # Чтение содержимого файла
        with open(filename[1:], 'rb') as f:
            outputdata = f.read()

        # Отправляем HTTP-заголовок ответа клиенту
        header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        connectionSocket.send(header.encode())

        # Отправляем содержимое запрошенного файла клиенту
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i + 1])

        # Закрываем соединение с клиентом
        connectionSocket.close()
    except IOError:
        # В случае отсутствия файла на сервере отправляем сообщение об ошибке клиенту
        error_header = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n"
        connectionSocket.send(error_header.encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
        connectionSocket.close()

# Создаем сокет сервера
serverSocket = socket(AF_INET, SOCK_STREAM)

# Задаем порт сервера
serverPort = 8080

# Привязываем серверный сокет к порту
serverSocket.bind(("", serverPort))

# Запускаем прослушивание серверным сокетом
serverSocket.listen(5)

# Ожидаем клиента
while True:
    print("Готов к обслуживанию...")
    
    # Устанавливаем соединение с клиентом
    connectionSocket, addr = serverSocket.accept()

    # Создаем новый поток для обработки клиента
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
    
    # Запускаем поток
    client_thread.start()

# Закрываем сокет сервера
serverSocket.close()

# http://localhost:8080/hw.html