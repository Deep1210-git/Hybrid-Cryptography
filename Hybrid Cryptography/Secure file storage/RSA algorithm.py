import secrets
import random
import binascii
import sys
from Crypto.Cypher import AES



def gcd(a, b):
        '''Euclid's algorithm '''
        while b != 0:
            temp=a % b
            a=b
            b=temp
        return a

def multiplicativeInverse(a, b):
        """Euclid's extended algorithm"""
        x = 0
        y = 1
        lx = 1
        ly = 0
        oa = a 
        ob = b  
        while b != 0:
            q = a // b
            (a, b) = (b, a % b)
            (x, lx) = ((lx - (q * x)), x)
            (y, ly) = ((ly - (q * y)), y)
        if lx < 0:
            lx += ob  
        if ly < 0:
            ly += oa  
        return lx

def generatePrime(keysize):
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))
        if isPrime(num):
            return num

def isPrime(num):
    if (num < 2):
        return False # 0, 1, and negative numbers are not prime
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 
                 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 
                 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 
                 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 
                 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 
                 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 
                 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 
                 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 
                 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    
    if num in lowPrimes:
        return True
    
    for prime in lowPrimes:
        if (num % prime == 0):
            return False
    
    return millerRabin(num)


def millerRabin(n, k = 7):
    if n < 6:  
        return [False, False, True, True, False, True][n]
    elif n & 1 == 0:  
        return False
    else:
      s, d = 0, n - 1
      while d & 1 == 0:
         s, d = s + 1, d >> 1
      for a in random.sample(range(2, min(n - 2, sys.maxsize)), min(n - 4, k)):
         x = pow(a, d, n)
         if x != 1 and x + 1 != n:
            for r in range(1, s):
               x = pow(x, 2, n)
               if x == 1:
                  return False 
               elif x == n - 1:
                  a = 0  
                  break 
            if a:
               return False  
      return True  

def KeyGeneration(size):
    
    #1)Generate 2 large random primes p,q (same size)
    p=generatePrime(keysize)
    q=generatePrime(keysize)
    if not (isPrime(p) and isPrime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    #2)compute n=pq and phi=(p-1)(q-1)
    n = p * q
    phi = (p-1) * (q-1)

    #3) select random integer "e" (1<e<phi) such that gcd(e,phi)=1
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #4)Use Extended Euclid's Algorithm to compute another unique integer "d" (1<d<phi) such that e.d≡1(mod phi)
    d = multiplicative_inverse(e, phi)
    
    #5)Return public and private keys
    #Public key is (e, n) and private key is (d, n)
    return ((n, e), (d, n))

def encrypt(pk, plaintext):
    #1) obtain (n,e) 
    n, e = pk
    #2)message space [0,n-1]
    #3)compute c=m^e
    c = [(ord(char) ** e) % n for char in plaintext]
    #4) send "C" to the other party
    return c

def decrypt(pk, ciphertext):
    d, n = pk
    #5)m=c^d
    m = [chr((char ** d) % n) for char in ciphertext]
    return ''.join(m) 

def main():
    keyAES = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    print ('keyAES', [x for x in key])
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])

    keysize = int(input("Enter a key size "))
    pub,pri=keyGeneration(keysize)
    plainText = input("Enter the Plain text: ")
    cipher=encrypt(pub,plainText)
    print("Cipher text: ")
    print(cipher)
    p=decrypt(pri,cipher)
    print("decrypted message: ")
    print("p")
    input('Press ENTER to exit')

if __name__ == "__main__":
    main()