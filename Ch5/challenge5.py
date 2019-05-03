import sys
import numpy as np

keyboard = {'1': (0, 0), '2': (0, 1), '3': (0, 2), '4': (0, 3), '5': (0, 4), '6': (0, 5), '7': (0, 6), '8': (0, 7), '9': (0, 8), '0': (0, 9),
            'Q': (1, 0), 'W': (1, 1), 'E': (1, 2), 'R': (1, 3), 'T': (1, 4), 'Y': (1, 5), 'U': (1, 6), 'I': (1, 7), 'O': (1, 8), 'P': (1, 9),
            'A': (2, 0), 'S': (2, 1), 'D': (2, 2), 'F': (2, 3), 'G': (2, 4), 'H': (2, 5), 'J': (2, 6), 'K': (2, 7), 'L': (2, 8), ';': (2, 9),
            'Z': (3, 0), 'X': (3, 1), 'C': (3, 2), 'V': (3, 3), 'B': (3, 4), 'N': (3, 5), 'M': (3, 6), ',': (3, 7), '.': (3, 8), '-': (3, 9)}
reversed_keyboard = dict(map(reversed, keyboard.items()))
def getShift(codedKey, letraOrig):
    codedKeyPos = keyboard[codedKey]
    originalPos = keyboard[letraOrig]
    return (originalPos[0]-codedKeyPos[0],originalPos[1]-codedKeyPos[1])

def decode(letra, shift):
    letraPos = keyboard[letra]
    nuevaPos = tuple(np.add(letraPos, shift))
    nuevaPos = (nuevaPos[0]%4, nuevaPos[1]%10)
    return reversed_keyboard[nuevaPos]

if __name__ == "__main__":
    readFile = open(sys.argv[1], "r")
    writeFile = open("out.txt", "w")

    numeroCasos = int(readFile.readline())
    for caso in range(1, numeroCasos+1):
        letraOrig = readFile.readline().replace("\n","").replace("\t","")
        print(letraOrig)
        carta = readFile.readline().strip()
        codedKey = carta[-1]   
        shift = getShift(codedKey, letraOrig)
        cartaTraducida = ""
        for letra in carta:
            if letra == " ":
                cartaTraducida+=letra
            else:
                cartaTraducida+=decode(letra,shift)
        writeFile.write("Case #%i: %s\n" % (caso, cartaTraducida))
        print("Case #%i: %s\n" % (caso, cartaTraducida))