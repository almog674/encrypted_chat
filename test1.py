from cryptography import RSA
from cryptography import Three_des
from queue import Queue
import threading
import time
import timer


almog = RSA()
public_key = None
while not public_key:
    public_key, privet_key, n = almog.generate_keys()
print(f'public key: {public_key}, privet_key: {privet_key}')

des = Three_des()
key_list = des.generate_keys()
cipher_key_list = []
decrypted_key_list = []
for key in key_list:
    cipher_key = almog.encrypt(public_key, n, key)
    cipher_key_list.append(cipher_key)

for key in cipher_key_list:
    decrypted_key = almog.decrypt(privet_key, n, key)
    decrypted_key_list.append(decrypted_key)

print(key_list)
print(decrypted_key_list)

# roee = Three_des()
# key_list = roee.generate_keys()
# IV, cipher_text = roee.encrypt('almog maimonasdfgdhfjgkh', key_list)
# decrypted_text = roee.decrypt(cipher_text, key_list, IV)
# print(decrypted_text)
