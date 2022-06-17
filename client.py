import socket
import threading
import tkinter
import time
import sys
from cryptography import RSA, Three_des
from tkinter_moduls import Sing_In, Sing_Up, Start

print(2 ** 2 ** 2 ** 2 ** 2)

IP = '127.0.0.1'
PORT = 9999

class Client:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.rsa = RSA()
        self.public_key, self.privet_key, self.n = self.rsa.generate_keys()
        self.sessions = []
        self.admin = False
        self.username, self.password = self.get_username_and_password()


    def get_username_and_password(self):
        validated_username = 0
        validated_password = 0
        while (not validated_username) and (not validated_password):
            starter_window = Start()
            if not starter_window.choose:
                break
            elif starter_window.choose == 'sing_up':
                self.sing_up()

    # def sing_up():
    #     window = 
                

almog = Client(IP, PORT)