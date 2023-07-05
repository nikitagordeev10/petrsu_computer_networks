from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)

# Подготавливаем сокет сервера
serverPort = 8000
serverSocket.bind(("", serverPort))
serverSocket.listen(5) # максимальное количество ожидающих запросов

while True:
    # Устанавливаем соединение
    print("Готов к обслуживанию...")
    connectionSocket, addr = serverSocket.accept() # в бесконечном цикле ожидается подключение клиента
    try:
        message = connectionSocket.recv(1024) #  запрос от клиента
        filename = message.split()[1] #  имя запрашиваемого файла
        with open(filename[1:], 'rb') as f: # если файл существует
            outputdata = f.read() # читаем

        # Отправляем в сокет одну строку HTTP-заголовка
        header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        connectionSocket.send(header.encode())

        # Отправляем содержимое запрошенного файла клиенту
        for i in range(0, len(outputdata)):
            try:
                connectionSocket.send(outputdata[i:i + 1])
            except (ConnectionResetError, BrokenPipeError):
                print('Client closed the connection.')
                connectionSocket.close()
                break

        connectionSocket.close()
    except IOError: # файл не существует
        # Отправляем ответ об отсутствии файла на сервере
        error_header = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n"
        try:
            connectionSocket.send(error_header.encode())
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
        except (ConnectionResetError, BrokenPipeError):
            print('Client closed the connection.')

    # Закрываем клиентский сокет
    connectionSocket.close() # 

serverSocket.close() # данные были отправлены клиенту, соединение разрывается

# http://localhost:8080/site_1.html