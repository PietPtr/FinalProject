# sorry for not adding it properly, Simon please fix?

import math
import random
import decimal

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]

EXPONENT = 17
SIZE_N = 128
MILLER_RABIN_ROUNDS = 40

primeP = 0
primeQ = 0
n      = 0
phi    = 0
d      = 0

def millerRabinFase1(number):
    """ removes all numbers which are not prime, based on trial division """
    if number % 2 == 0:
        return False
    else:
        for i in range(0, len(primes)):
            if(number % primes[i] == 0 and number != primes[i]):
                return False
    return True

def millerRabinFase2(number, rounds):
    """ Performs miller rabin rounds """
    if number % 2 == 0:
        return False
    s = 0
    d = number-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    def tryMillerRabin(a):
        if modExp(a, d, number) == 1:
            return False
        for i in range(s):
            if modExp(a, 2**i * d, number) == number-1:
                return False                # n might be prime
        return True                         # n definitly not prime
    for i in range(rounds):
        a = random.randrange(2,number-2)
        if tryMillerRabin(a):
            return False
    return True


def isPrime(number, rounds):
    """ First executes trial division based on lookup-table of primes, then performs miller rabin rounds"""
    if millerRabinFase1(number):
        if millerRabinFase2(number, rounds):
            return True
    return False


def genPrime (bitsize, rounds):
    """ Generates a random prime, with atleast bitsize number of bits, and tests primality with isPrimeComplex function"""
    q = random.randrange(2**bitsize, 2**(bitsize+1))
    if q % 2 == 0:
        q += 1
    
    # there is no need to cbange to random primes, +2 is good enough, even though it has a bias to primes after a large gap
    while not isPrimeComplex(q, rounds):
        q += 2
    return q


def extendedEuclidean(a, b):
    """ Performs extended euclidean algorithm """
    oldb = b
    olda = a
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
    # makes sure the output of the function is positive / performs modulo function to make numbers positive
    x0 = x0 % oldb
    y0 = y0 % olda
    
    return a, x0, y0

def getDecryptionKey(e, phi):
    """ Gets the decryption key corresponding to the encryption key e, the euleur totient of n"""
    _, d, _ = extendedEuclidean(e, phi)
    return d

def modExp(a,b,n):
    """ calculate a^b mod n, python libery also has this function, but yeah"""
    i = 1
    accumulator = 1
    
    #array containing all the values of a**(2**i) mod n
    mods = [a % n]
    
    # calculate all modulo's off the power of 2's up to b
    while 2**i <= b:
        mods.append((mods[i-1] ** 2) % n)
        i += 1
        
    # multiply all the modulo's needed to make the number n
    while b > 0:
        if b >= 2**i:
            b -= 2**i
            accumulator *= mods[i]
            accumulator %= n
        i -= 1
    return accumulator

def init():
    global primeP
    primeP = genPrime(SIZE_N / 2, MILLER_RABIN_ROUNDS)
    global primeQ
    primeQ = genPrime(SIZE_N / 2, MILLER_RABIN_ROUNDS)
    global phi 
    phi = (primeP-1) * (primeQ-1)

    while phi % EXPONENT == 0:
        ## print("phi is divisable by exponent, automatic retry")
        
        primeQ = genQ(SIZE_N-sizeP, MILLER_RABIN_ROUNDS)
        phi = (primeP-1) * (primeQ-1)
    global n
    n = primeP * primeQ
    global d
    d = getDecryptionKey(EXPONENT, phi)

    ## SEND THE n SIMON PLEASE WORK MAGIC?!
    # send n to arduino

def decrypt(uid):
    message = modExp(uid, d, n);
    
    




