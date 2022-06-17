import math
import time

def is_prime(number):
    if number == 1:
        return False

    max_divisor = math.floor((math.sqrt(number)))

    if number == 2:
        return True
    
    if number > 2 and number % 2 == 0:
        return False
    
    for i in range(3, max_divisor, 2):
        if number % i == 0:
            return False
    return True


t0 = time.time()
for n in range(2 ** (128 - 1),(2 ** 128) - 1):
    almog = is_prime(n)
    if almog == True:
        print(almog)
        break
    else:
        print(n)
        time.sleep(.5)
t1 = time.time()
time = (t1 - t0)
print(time)

