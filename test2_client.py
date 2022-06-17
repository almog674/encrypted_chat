import socket
import threading
import time
import sys
from cryptography import Three_des
from cryptography import RSA

IP = '127.0.0.1'
PORT = 6666

class Client:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.nickname = self.get_nickname()
        self.des = Three_des()
        self.rsa = RSA()
        self.public_key, self.privet_key, self.n = self.rsa.generate_keys()
        self.settings = {
        'manager': False,
        'mute': False,
        'kicked': False
        }
        self.client = self.initialize_client(self.IP, self.PORT)

        receive_thread = threading.Thread(target = self.recieve)
        receive_thread.start()

        write_thread = threading.Thread(target = self.write)
        write_thread.start()

    def initialize_client(self, IP, PORT):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        return client

    def get_nickname(self):
        nickname = input('What is your name? ')
        while '@' in nickname:
            print('[SYSTEM] you cant use the character "@" ')
            nickname = input('What is your name?')
        return nickname

    def get_message_type(self):
        message_type = input('')
        return message_type

    def broadcast_message(self, message_type, nickname_length):
        print('You can write a message')
        message = input('')
        if '[' in message or ']' in message:
            print("You can't use the characters '[]'")
            return 
        (iv, cipher_message) = self.des.encrypt(message, self.key_list)
        full_cipher_message = f'{cipher_message}#{iv}'
        full_message = f'{nickname_length}{self.nickname}{message_type}{full_cipher_message}'
        self.client.send(full_message.encode())

    def disconnect(self):
        self.client.close()
        
    def make_privet_message(self, recipient, message_type, nickname_length):
        print('You can write a message')
        message = input('')
        if '[' in message or ']' in message:
            print("You can't use the characters '[]'")
            return
        (iv, cipher_message) = self.des.encrypt(message, self.key_list)
        full_cipher_message = f'{cipher_message}#{iv}'
        full_message = f'{nickname_length}{self.nickname}{message_type}{full_cipher_message}/{recipient}'
        return full_message

    def send_image(self, message_type, nickname_length):
        print('What is the image url?')
        url = input('')
        image = open(url, 'rb')
        image_data = image.read(1024)
        while image_data:
            full_message = f'{nickname_length}{self.nickname}{message_type}{image_data}'
            self.client.send(full_message.encode())
            image_data = image.read(2048)

        

    def privet_message(self, recipient, message_type, nickname_length):
        message = self.make_privet_message(recipient, message_type, nickname_length)
        if message:

            self.client.send(message.encode())

    def check_managers(self, message_type, nickname_length):
        message_content = ''
        message = f'{nickname_length}{self.nickname}{message_type}{message_content}'
        self.client.send(message.encode())

    def change_user_settings(self, message_type, nickname_length, message):
        print(message)
        recipient = input('')
        message = ' '
        full_message = f'{nickname_length}{self.nickname}{message_type}{message}/{recipient}'
        self.client.send(full_message.encode())

    def write(self):
        time.sleep(1.5)
        while True:
            message_type = self.get_message_type()
            nickname_length = len(self.nickname)
            if message_type.isdigit() == False:
                print('[SYSTEM] Only digits allowd')
            elif (int(message_type) > 4) and (self.settings['manager'] == 'False'):
                print('You cannot use this command!')
            elif (message_type == '1') and (self.settings['mute'] == 'False'):
                self.broadcast_message(message_type, nickname_length)
            elif (message_type == '2') and (self.settings['mute'] == 'False'):
                print('Who you want to send to?')
                recipient = input('')
                self.privet_message(recipient, message_type, nickname_length)
            elif message_type == '3':
                self.check_managers(message_type, nickname_length)
            elif message_type == '4':
                self.client.close()
                print('[SYSTEM] disconnected successfuly')
                sys.exit()
            elif message_type == '5':
                self.change_user_settings(message_type, nickname_length, "Who's the user you want to kick? ")
            elif message_type == '6':
                self.change_user_settings(message_type, nickname_length, "Who's the user you want to make a manager? ")
            elif message_type == '7':
                self.change_user_settings(message_type, nickname_length, "Who's the user you want to mute? ")
            elif message_type == '8':
               self.change_user_settings(message_type, nickname_length, "Who's the user you want to unmute? ") 
            elif message_type == '9':
                self.send_image(message_type, nickname_length)
            elif (3 > int(message_type) > 0) and (self.settings['mute'] == 'True'):
                print('You are muted')
            else:
                print('[SYSTEM] Unknown command')

            

    def recieve(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message == 'NICK':
                    self.client.send(self.nickname.encode())
                elif '[START]' in message:
                    message_split = message.split(sep = '/')
                    manager = message_split[1]
                    mute = message_split[2]
                    kicked = message_split[3]
                    self.settings['manager'] = manager
                    self.settings['mute'] = mute
                    self.settings['kicked'] = kicked
                elif '[KICKED]' in message:
                    self.client.close()
                    sys.exit()
                elif '[MANAGER]' in message:
                    self.settings['manager'] = 'True'
                elif '[MUTE]' in message:
                    self.settings['mute'] = 'True'
                elif '[UNMUTE]' in message:
                    self.settings['mute'] = 'False'
                elif '[KEYS]' in message:
                    self.key_list = []
                    message_split = message.split(sep = '/')
                    key_part = message_split[1]
                    key_part_split = key_part.split(sep = "'")
                    self.cipher_key_list = [key_part_split[1], key_part_split[3], key_part_split[5]]
                    for key in self.cipher_key_list:
                        decrypted_key = self.rsa.decrypt(self.privet_key, self.n, key)
                        self.key_list.append(decrypted_key)
                    print(self.key_list)
                        
                        
                elif '[PUBLIC]' in message:
                    print(self.public_key)
                    message = f'{str(self.public_key)}/{str(self.n)}'
                    self.client.send(message.encode())
                elif '#' in message:
                    seperated_message = message.split(':')
                    info = seperated_message[0] + ':' +  seperated_message[1] +  ': '
                    cipher_message_content = seperated_message[2]
                    seperated_message_content = cipher_message_content.split('#')
                    cipher_message = seperated_message_content[0]
                    IV = seperated_message_content[1]
                    decrypted_message = self.des.decrypt(cipher_message, self.key_list, IV)
                    message_to_show = info + decrypted_message
                    print(message_to_show)
                else:
                    print(message)
            except:
                print('[SYSTEM] something went wrong...')
                self.client.close()
                break
        self.client.close()

roee = Client(IP, PORT)