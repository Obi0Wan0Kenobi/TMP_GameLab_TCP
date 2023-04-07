import random
import socket
import threading
import time

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

critical_section = threading.Lock()
usermas= {}

#rock - 1
#cisors - 2
#paper - 3

class Player:
    def __init__(self,ip,port):
        busy=False
        playwith=0
        id = random.randint(1,200)
        with critical_section:
            while id in usermas.keys():
                id = random.randint(1, 200)
        with critical_section:
            for i in usermas.values():
                if i.id!=id and i.busy==False:
                    usermas[i.id].playwith = id
                    usermas[i.id].busy = True
                    busy = True
                    playwith = i.id

        self.id = id
        self.busy = busy
        self.playwith = playwith
        self.ip = ip
        self.port = port
        self.selected=0
        self.checked=False


    def find_game(self):
        finded=True
        while finded:
            time.sleep(1)
            with critical_section:
               if self.busy == True:
                   return self.playwith


    def select(self,numselected):
        self.selected=numselected

    def win_or_not(self):
        finded = True
        while finded:
            time.sleep(1)
            with critical_section:
                #print(usermas[self.playwith].selected)
                if usermas[self.playwith].selected != 0:
                    if usermas[self.playwith].selected==1 and self.selected==3:
                        return True
                    if usermas[self.playwith].selected==2 and self.selected==1:
                        return True
                    if usermas[self.playwith].selected==3 and self.selected==2:
                        return True
                    return False

def handle_client(client_socket, client_address):
    player=0
    try:
        while True:

            data = client_socket.recv(1024)
            print(f'Received from {client_address}: {data.decode()}')
            if data.decode()!="ok":
                print(f"Соединение разорвано с {client_address}")
                exit()
            player = Player(client_address,"0")
            with critical_section:
                usermas[player.id]=player
            client_socket.send(str(player.id).encode())
            if player.busy==False:
                player.playwith = usermas[player.id].find_game()

            client_socket.send(str(f"Вы играете с {str(player.playwith)}").encode())
            data = client_socket.recv(1024)
            if data.decode()=="start":
                client_socket.send(str("Okey:start").encode())

            choosed =True
            while choosed:
                choosen = client_socket.recv(1024)
                try:
                    choosennum=int(choosen.decode())
                    choosed=False
                except:
                    client_socket.send(str("Введите число!").encode())

            with critical_section:
                usermas[player.id].select(choosennum)
            client_socket.send(str("wait").encode())

            result=usermas[player.id].win_or_not()
            client_socket.send(str(f"Вы выиграли = {str(result)}").encode())








    except Exception as err:
        print(f"Соединение разорвано с {client_address}")
        with critical_section:
            del usermas[player.id]
            print(usermas)
        if(str(err) == "[WinError 10053] Программа на вашем хост-компьютере разорвала установленное подключение"):
            pass




server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.bind((SERVER_ADDRESS, SERVER_PORT))


server_socket.listen()

while True:
    client_socket, client_address = server_socket.accept()
    print(f'Connected from {client_address}')
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()