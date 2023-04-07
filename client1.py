import socket
import threading

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345


def send_data(client_socket):
    while True:

        client_socket.send(b'ok')

        response = client_socket.recv(1024)
        print(f'Ваш айди: {response.decode()}')
        response = client_socket.recv(1024)
        print(f'{response.decode()}')
        client_socket.send(str("start").encode())
        response = client_socket.recv(1024)
        if response.decode()!="Okey:start":
            print("err")
            return
        message = input('rock - 1; cisors - 2; paper - 3 : ')
        client_socket.send(message.encode())

        choosed = True
        while choosed:
            choosen = client_socket.recv(1024)
            if choosen.decode()=="wait":
                choosed = False
            else:
                message = input('rock - 1; cisors - 2; paper - 3 : ')
                client_socket.send(message.encode())

        finish = client_socket.recv(1024)
        print(finish.decode())

        reload = input("Хотите сыграть еще ? 1-да 0-нет: ")
        if reload=="0":
            exit()
        print("===========================================")





client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client_socket.connect((SERVER_ADDRESS, SERVER_PORT))


client_thread = threading.Thread(target=send_data, args=(client_socket,))
client_thread.start()


client_thread.join()
client_socket.close()