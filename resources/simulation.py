'''
15643 - THOMAS Mathéo
TIPE - Code correcteur d'erreur

Simulation de la transmission d'un signal subissant une perturbation
'''

###########
# IMPORTS #
###########
import numpy as np
import matplotlib.pyplot as plt
import random 
import scipy.fft as sfft

#######
# DAC #
#######
treshold = 0.5

def alphaToBinary(msg):     # convertit un message alphanumérique en binaire (code ASCII)
    n = len(msg)
    res = ''
    for i in range(n):
        res += (f'{ord(msg[i]):08b}')
    return res

def binaryToAnalog(msg):    # crée un signal temporel à partir d'un message binaire (1 -> 1 in binary, -1 -> 0 in binary)
    N = 10*len(msg)
    n = len(msg)
    tab = np.linspace(0,0, N)
    cut = 0
    for i in range(n):
        #if i % 8 == 0:
        #    cut += 10
        for j in range(10):
            if msg[i] == "1":
                tab[10*i+j+cut] = 1
            else:
                tab[10*i+j+cut] = -1
    return tab

def alphaToAnalog(m):       # conversion alphanumérique - 'analogique'
    return binaryToAnalog(alphaToBinary(m))


def binaryToAlpha(msg):     # convertit un message binaire en alphanumérique (code ASCII)
    res2 = ""
    n = len(msg)
    for i in range(n//8):
        res1 = 0
        n = 8
        for j in range(8):
            res1 += 2**(n-1)*int(msg[j+8*i])
            n -= 1
        res2 += chr(res1)
    return res2

def analogToBinary(tab):    # convertit un signal temporel en binaire (1 -> 1 en binaire, -1 -> 0 en binaire)
    N = len(tab)
    i = 1
    res = ""
    while i < N:
        if tab[i] >= treshold:
            res += "1"
        else:
            res += "0"
        i += 10
    return res

def analogToAlpha(tab):     #conversion 'analogique' - alphanumérique
    return binaryToAlpha(analogToBinary(tab))


###########
# HAMMING #
###########
def add(x, y):              # XOR
    if x == y:
        return '0'
    else:
        return '1'

def encode(msg):            # calcule les bits de parité pour encoder msg
    msg += add(add(msg[0],msg[1]), msg[3])
    msg += add(add(msg[0],msg[2]), msg[3])
    msg += add(add(msg[1],msg[2]), msg[3])
    return msg

def encoder(msg):
    res = ''
    chunks, chunk_size = len(msg), 4
    m = [ msg[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    for i in range(len(msg)//4):
        res += encode(m[i])
    return res

def opp(msg, i):            # inverse le bit de msg en position i
    l = list(msg)
    if l[i] == '1':
        l[i] = '0'
    else:
        l[i] = '1'
    return "".join(l)

def decode(msg):            # calcule et compare les bits de parité, et modifie en conséquence msg pour le corriger
    w4 = add(add(msg[0],msg[1]), msg[3])
    w5 = add(add(msg[0],msg[2]), msg[3])
    w6 = add(add(msg[1],msg[2]), msg[3])

    if w4 != msg[4] and w5 != msg[5] and w6 != msg[6]:
        # print("msg[3] false")
        return opp(msg, 3)
    elif w4 != msg[4] and w5 != msg[5]:
        # print("msg[0] false")
        return opp(msg, 0)
    elif w4 != msg[4] and w6 != msg[6]:
        # print("msg[1] false")
        return opp(msg, 1)
    elif w5 != msg[5] and w6 != msg[6]:
        # print("msg[2] false")
        return opp(msg, 2)
    elif w4 != msg[4]:
        # print("msg[4] false")
        return opp(msg, 4)
    elif w5 != msg[5]:
        # print("msg[5] false")
        return opp(msg, 5)
    elif w6 != msg[6]:
        # print("msg[6] false")
        return opp(msg, 6)
    # print("msg correct")
    return msg

def decoder(msg):
    res = ''
    chunks, chunk_size = len(msg), 7
    m = [ msg[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    for i in range(len(msg)//7):
        res += (decode(m[i]))[0:4]
    return res

def perturb(msg):           # inverse un bit de msg au hasard
    r = random.randint(0, len(msg))
    print ("bit modifié :", r)
    return opp(msg, r)

def perturbAnalog(tab):
    r = (random.randint(0, len(tab)))//10
    print("r : ", r)
    for i in range(10):
        if (tab[r*10 + i] == 1):
            tab[(r*10)+i] = -1
        else :
            tab[(r*10)+i] = 1
    return tab

def perturbAnalogMulti(tab):
    print("perturbations : ", len(tab)//200)
    for i in range(len(tab)//200):
        tab = perturbAnalog(tab)
    return tab 

def perturbAnalogMultiEvenly(tab):
    for j in range((len(tab))//140):
        r = random.randint(j*14, (j+1)*14)
        for i in range(10):
            if (tab[r*10 + i] == 1):
                tab[(r*10)+i] = -1
            else :
                tab[(r*10)+i] = 1
    return tab

def fft(t, s):              # renvoie la décomposition en série de fourier du signal s où f est un tableau de fréquences et a est un tableau d'amplitudes complexes décrivant le signal # Paramètres : t : tab[float], points - s : tab[float], le signal s evalué en tous les points de t
    N, fe = len(t), 1/(t[1]-t[0])
    a = sfft.fft(s)
    f = sfft.fftfreq(N, 1/fe)
    return f, a


#############
# EXECUTION #
#############
# 1. Message initial
m = "Hello, World !"
print("Message initial : ", m)
atb = alphaToBinary(m)
print("Message converti en binaire : ", atb)

# 2. Codage du message avec le code de Hamming
encodemsg = encoder(atb)
print("Message encodé : ", encodemsg)

# 3. Conversion numérique-analogique
analogmsg = binaryToAnalog(encodemsg)

plt.figure(1)
plt.title("Signal analogique émis")
plt.xlabel("Temps")
plt.ylabel("Amplitude")

plt.plot(analogmsg)

# 4. Perturbation 
# analogmsg = perturbAnalog(analogmsg)
# analogmsg = perturbAnalogMulti(analogmsg)
analogmsg = perturbAnalogMultiEvenly(analogmsg)     # Ajout d'erreurs sur les bits (inversion)
plt.plot(analogmsg)
plt.legend(["Signal initial", "Signal perturbé"], loc = "upper right")

analogmsgNoise = analogmsg + np.random.normal(0, .1, len(analogmsg))    # Ajout de bruit sur tout le spectre

plt.figure(2)
plt.title("Signal analogique reçu")
plt.xlabel("Temps")
plt.ylabel("Amplitude")
plt.plot(analogmsgNoise)

x = np.linspace(0, 1, len(analogmsg))

plt.figure(3)
plt.title("Transformée de Fourier (image agrandie)")
plt.xlabel("Fréquence")
plt.ylabel("Amplitude")
f1, an = fft(x, analogmsgNoise)
f2, a = fft(x, analogmsg)
plt.plot(f2, np.abs(a), f1, np.abs(an))
# plt.xlim(left=0)
plt.xlim(left=100, right =150)
plt.ylim(0, 210)
plt.legend(["Signal initial", "Signal perturbé"])

# 5. Conversion analogique-numérique
decodemsg = analogToBinary(analogmsgNoise)
print("Message perturbé numérique : ", decodemsg)

# 6. Correction du message
msg = decoder(decodemsg)
print("Message corrigé", msg)

# 7. Message final
mf = binaryToAlpha(msg)
print("Message final : ", mf)