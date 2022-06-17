import socket
import threading
import time
from cryptography import Three_des
from cryptography import RSA

IP = '0.0.0.0'
PORT = 6666

class Server:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.clients = []
        self.nicknames = []
        self.kick = False
        self.managers = ['almog674', 'roee90']
        self.des = Three_des()
        self.rsa = RSA()
        self.public_key, self.privet_key, self.n = self.rsa.generate_keys(20)
        self.key_list = self.des.generate_keys()
        print(self.key_list)
        server = self.initialize_server(self.IP, self.PORT)
        while True:
            self.get_time()
            client = self.handle_connection(server)


    def initialize_server(self, IP, PORT):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP, PORT))
        server.listen()
        print('[SYSTEM] server is up and ready!')
        return server

    def get_time(self):
        current_time = time.strftime('%H:%M', time.gmtime())
        return current_time


    def check_manager(self, user_nickname):
        for nickname in self.managers:
            if nickname == user_nickname:
                return "manager"
        return "member"


    def get_nickname(self, client):
        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        return nickname

    def send_init_message(self, client, nickname, user_type):
        message = """\n[SERVER] Hello """ + nickname +  """ welcome to the chat!
You are a """ + user_type + """
There are 8 commands which you can use:
    1: Broadcast message
    2: Privet message
    3: Check who is manager
    4: Disconnect the chat
    5: Kick user (only for managers)
    6: Make manager (only for managers)
    7: Mute user (only for managers)
    8: Unmute user (only for managers)
Enjoy!\n\n"""
        client.send(message.encode())

    def encrypt_keys(self, client, public_key, n):
        cipher_key_list = []
        for key in self.key_list:
            cipher_key = self.rsa.encrypt(int(public_key), int(n), str(key))
            cipher_key_list.append(cipher_key)
        return cipher_key_list

    def send_keys(self, client, cipher_key_list):
        key_message = f'[KEYS]/{cipher_key_list}'
        client.send(key_message.encode())

    def set_settings_message(self, client, user_type = False, silence = False, kicked = False):
        message_start = '[START]'
        if user_type == 'manager':
            manager = True
        else:
            manager = False
        message = f'{message_start}/{manager}/{silence}/{kicked}'
        client.send(message.encode())
        

    def seperate_client_sended(self, client_sended, clients):
        clients_to_send = []
        for client in clients:
            clients_to_send.append(client)
        if client_sended in clients_to_send:
            clients_to_send.remove(client_sended)
        return clients_to_send

    def build_broadcast_message(self, nickname, current_time, message):
        message = f'{current_time} {nickname}: {message}'
        return message

    def send_broadcast_message(self, message, clients_to_send):
        for client in clients_to_send:
            client.send(message.encode())


    def broadcast_message(self, nickname, clients, current_time, client, message, alert = False):
        clients_to_send = self.seperate_client_sended(client, self.clients)
        message = self.build_broadcast_message(nickname, current_time, message)
        self.send_broadcast_message(message, clients_to_send)
        if alert == False:
            client.send('[SERVER] sended succesfuly'.encode())

        

    def split_message(self, message, nickname, client):
        nickname_len = len(nickname)
        message_name_len = message[0 : len(str(nickname_len))]
        message_name = message[len(str(nickname_len)) : len(str(nickname_len)) + (nickname_len)]
        message_command = message[len(str(nickname_len)) + (nickname_len) : len(str(nickname_len)) + (nickname_len) + 1]
        message_content = message[len(str(nickname_len)) + (nickname_len) + 1 : len(message)]
        manager = self.check_if_manager(client)
        if manager == True:
            message_name = message_name + "@"
        return (message_name_len, message_name, message_command, message_content)

    def discconect_client(self, nickname, nickname_sended, clients, current_time, client, message):
        try:
            self.nicknames.remove(nickname)
            self.clients.remove(client)
            self.broadcast_message(nickname_sended, clients, current_time, client, message, True)
        except:
            pass

    def seperate_privet_message(self, message_content):
        split_message = message_content.split(sep = '/')
        message_content = split_message[0]
        recipient = split_message[1]
        return (message_content, recipient)

    def check_nickname_exists(self, nickname):
        for nick in self.nicknames:
            if nick == nickname:
                return True
        return False

    def find_client_with_nickname(self, nickname):
        index = self.nicknames.index(nickname)
        client_to_send = self.clients[index]
        return client_to_send

    def find_nickname_with_client(self, client):
        index = self.clients.index(client)
        nickname_to_send = self.nicknames[index]
        return nickname_to_send

    def privet_message(self, nickname, clients, current_time, client, message_content):
        message_content, recipient = self.seperate_privet_message(message_content)
        valid = self.check_nickname_exists(recipient)
        if valid == True:
            client_to_send = self.find_client_with_nickname(recipient)
            nickname = "!" + nickname
            message = self.build_broadcast_message(nickname, current_time, message_content)
            client_to_send.send(message.encode())
            client.send('[SERVER] sended succesfuly'.encode())
        if valid == False:
            client.send(f'[SERVER] the user {recipient} does not exists...'.encode())

    def check_managers(self, client):
        message = ''
        for manager in self.managers:
            connected = self.check_nickname_exists(manager)
            if connected == False:
                connected = 'disconnected'
            else:
                connected = 'connected'
            message = message + f'Manager: {manager} {connected}\n'
        client.send(message.encode())

    def check_if_manager(self, client):
        nickname = self.find_nickname_with_client(client)
        for manager in self.managers:
            if manager == nickname:
                return True
        return False

    def kick_user(self, client, nickname, clients, current_time, message_content):
        message_content, recipient = self.seperate_privet_message(message_content)
        valid = self.check_nickname_exists(recipient)
        if valid == True:
            client_to_send = self.find_client_with_nickname(recipient)
            message = f'You have kicked out by {nickname}'
            full_message = self.build_broadcast_message('[SERVER]', current_time, message)
            client_to_send.send(full_message.encode())
            client_to_send.send('[KICKED]'.encode())
            client_to_send.close()
            return nickname
        else:
            client.send(f'[SERVER] the user {recipient} does not exists...'.encode())

    def making_manager(self, client, nickname, clients, current_time, message_content):
        message_content, recipient = self.seperate_privet_message(message_content)
        valid = self.check_nickname_exists(recipient)
        if valid == True:
            client_to_send = self.find_client_with_nickname(recipient)
            is_manager = self.check_if_manager(client_to_send)
            if is_manager == False:            
                self.managers.append(recipient)
                self.broadcast_message('[SERVER]', self.clients, current_time, client, f'the user {nickname} made {recipient} a manager')
                client_to_send.send('[MANAGER]'.encode())
                recipient_index = self.nicknames.index(recipient)
                print(self.nicknames)
            else:
                client.send(f'[SERVER] the client {recipient} is already a manager!'.encode())
        else:
            client.send(f'[SERVER] the user {recipient} does not exists...'.encode())
        
    def mute_user(self, client, nickname, clients, current_time, message_content, message_type, message):
        message_content, recipient = self.seperate_privet_message(message_content)
        valid = self.check_nickname_exists(recipient)
        if valid == True:
            client_to_send = self.find_client_with_nickname(recipient)
            client_to_send.send(message_type.encode())
            full_message = self.build_broadcast_message('[SERVER]', current_time, message)
            client_to_send.send(full_message.encode())


    def handle_client(self, server, client, address, nickname):
        while True:
            current_time = self.get_time()
            try:
                message = client.recv(1024).decode()
                (message_name_len, message_name, message_command, message_content) = self.split_message(message, nickname, client)
                print(message_name)
                if message_command == '1':
                    self.broadcast_message(message_name, self.clients, current_time, client, message_content)
                elif message_command == '2':
                    self.privet_message(message_name, self.clients, current_time, client, message_content)
                elif message_command == '3':
                    self.check_managers(client)
                elif message_command == '4':
                    client.close()
                    self.kick = False
                elif message_command == '5':
                    kicker_user = self.kick_user(client, message_name, self.clients, current_time, message_content)
                    self.kick = True
                elif message_command == '6':
                    self.making_manager(client, message_name, self.clients, current_time, message_content)
                elif message_command == '7':
                    self.mute_user(client, message_name, self.clients, current_time, message_content, '[MUTE]', f'You have muted by {message_name}')
                elif message_command == '8':
                    self.mute_user(client, message_name, self.clients, current_time, message_content, '[UNMUTE]', f'You have unmuted by {message_name}')
                else:
                    print(message_command)
            except:
                if self.kick == False:
                    self.discconect_client(nickname, '[SERVER]', self.clients, current_time, client, f'{nickname} has quit the chat!')
                    break
                else:
                    self.discconect_client(nickname, '[SERVER]', self.clients, current_time, client, f'The user {nickname} has kicked by {nickname}')
                    break

    def get_public_key(self, client):
        message = '[PUBLIC]'
        client.send(message.encode())
        response = client.recv(1024).decode()
        print(response)
        response = response.split('/')
        public_key = response[0]
        n = response[1]
        return (public_key, n)        
    
           

    def handle_connection(self, server):
        client, address = server.accept()
        nickname = self.get_nickname(client)
        user_type = self.check_manager(nickname)
        self.set_settings_message(client, user_type)
        time.sleep(2)
        nickname = self.get_nickname(client)
        (public_key, n) = self.get_public_key(client)
        self.send_init_message(client, nickname, user_type)
        cipher_key_list = self.encrypt_keys(client, public_key, n)
        self.send_keys(client, cipher_key_list)
        print(f'[SERVER] {nickname} has joined the chat!')
        current_time = self.get_time()
        self.broadcast_message('[SERVER]', self.clients, current_time, client, f'The client {nickname} has joined the chat!', True)
        self.clients.append(client)
        self.nicknames.append(nickname)
        thread = threading.Thread(target = self.handle_client, args = (server, client, address, nickname))
        thread.start()
        print(f'[SYSTEM] there is {threading.activeCount() - 1} active connections')





almog = Server(IP, PORT)