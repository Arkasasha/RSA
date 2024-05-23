from pickle import FALSE
import random
import math
import os
 
# A set will be the collection of prime numbers,
# where we can select random primes p and q
prime = set()
 
public_key = None
private_key = None
n = None
 
def gcdExtended(a, b):
    # Base Case
    if a == 0:
        return b, 0, 1
 
    gcd, x1, y1 = gcdExtended(b % a, a)
 
    # Update x and y using results of recursive
    # call
    x = y1 - (b//a) * x1
    y = x1
 
    return gcd, x, y

def setkeys(p, q):
    
    n = p * q
    fi = (p - 1) * (q - 1)
 
    e = 2
    while True:
        num1 = e
        num2 = fi
        if(e < fi):
            num1 = fi
            num2 = e
        if gcdExtended(num2, num1)[0] == 1:
            break
        e += 1
 
    # d = (k*Φ(n) + 1) / e for some integer k
    public_key = e
 
    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1
 
    private_key = d
    
    return public_key, private_key, n

def encode(message, e, n):
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= n
        e -= 1
    return encrypted_text

def encrypt():
    print(f'Write two primary numbers: ')
    p = 0
    q = 0
    while True:
        p = int(input(f'First number:\n'))
        q = int(input(f'Second number:\n'))
        if gcdExtended(1, p)[0] == 1 and gcdExtended(1, q)[0] == 1:
            break
        else:
            print(f'Number are not primary. Try again.')
            print('\n')
    
    print(f'Write a text that has to be encrypted: ')
    plaintext = input()
    
    public_key, private_key, n = setkeys(p, q)
    print(f'Public key: ({public_key}, {n})')
    print(f'Private key: ({private_key}, {n})')
    
    print(f'Write a file name to save ciphertext: ')
    file_name = input()
    file_path = 'messages\\' + file_name + '.txt'

    with open(file_path, 'w') as f:
        f.write(f'{n}')
        f.write('\n')
        f.write(f'{public_key}')
        f.write('\n')
        for letter in plaintext:
            f.write(f'{encode(ord(letter), public_key, n)}')
            f.write('\n')

def primefiller():
    # Method used to fill the primes set is Sieve of
    # Eratosthenes (a method to collect prime numbers)
    prime = set()
    
    seive = [True] * 250
    seive[0] = False
    seive[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            seive[j] = False
 
    # Filling the prime numbers
    for i in range(len(seive)):
        if seive[i]:
            prime.add(i)
            
    return prime

def pick_prime_nums(n):
    primes = primefiller()
    p = 0
    q = 0

    for i in primes:
        for j in primes:
            if i * j == n:
                p = i
                q = j
                break
    if p == 0 and q == 0:
        print(f'Coudn\'t find prime numbers')
    else:
        e, d, n = setkeys(p, q)
        return d 

def decode(encrypted_text, d, n):
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted

def decrypt():
    print(f'Write a file name to be decrypted:')
    file_name = input()
    file_path = 'messages\\' + file_name + '.txt'
    
    public_key = 0
    private_key = 0
    n = 0
    s= ''

    if not os.path.exists(file_path):
        print(f'This file doen\'t exist')
    else:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()
                if line_number == 1:
                    n = int(line)
                    private_key = pick_prime_nums(n)
                if line_number == 2:
                    public_key = int(line)
                if line_number > 2:
                    s += chr(decode(int(line), private_key, n))
        print(s)    

def menu():
    end = False
    while True:
        os.system('cls')
        print(f'Choose an option')
        print(f'(1) Encrypt message')
        print(f'(2) Decrypt file')
        print(f'(3) End program')
        
        while True:
            choice = input()
            if choice == '1':
                encrypt()
                break
            if choice == '2':
                decrypt()
                break
            if choice == '3':
                end = True
                break
            if choice != '1' and choice != '2' and choice != '3':
                print(f'Wrong option. Try again')
        if end == True:
            break

if __name__ == '__main__':
    newpath = r'messages'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    menu()
