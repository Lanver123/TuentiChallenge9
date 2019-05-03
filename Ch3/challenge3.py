import sys
from collections import OrderedDict
import matplotlib.pyplot as plt

def printResult(points):
    x = []
    y = []
    for point in points:
        x += [point[0]]
        y += [point[1]]
    plt.scatter(x,y)
    left, right = plt.ylim()
    plt.ylim(right, left)

    plt.show()

def T(pos, W, H):
    pos1 = (pos[0], pos[1]+H)
    pos2 = (pos[0], H-pos[1]-1)
    return [pos1, pos2]


def B(pos, W, H):
    pos1 = (pos[0], pos[1])
    pos2 = (pos[0], 2*H-pos[1]-1)
    return [pos1, pos2]


def L(pos, W, H):
    pos1 = (W+pos[0], pos[1])
    pos2 = (W-pos[0]-1, pos[1])
    return [pos1, pos2]


def R(pos, W, H):
    pos1 = (pos[0], pos[1])
    pos2 = (2*W-pos[0]-1, pos[1])
    return [pos1, pos2]


if __name__ == "__main__":
    readFile = open(sys.argv[1], "r")
    writeFile = open("out.txt", "w")

    numeroCasos = int(readFile.readline())
    for caseNumber in range(1, numeroCasos+1):
        parametros = readFile.readline().split()
        parametros = list(map(int, parametros))
        comandos = []
        posiciones = []
        for _ in range(int(parametros[2])):
            comandosLeidos = readFile.readline().replace("\n","")
            comandos.extend(comandosLeidos)

        for _ in range(int(parametros[3])):
            posicion = readFile.readline().replace("\n","").split()
            posicion = list(map(int, posicion))
            posiciones.extend([posicion])
        
        posiciones = list(map(tuple, posiciones))
        for comando in comandos:
            numeroPos = len(posiciones)
            nuevasPos = []
            if comando is "L":
                for posicion in range(numeroPos):
                    nuevasPos += L(posiciones[posicion],parametros[0],parametros[1])
                parametros[0] *= 2
            if comando is "R":
                for posicion in range(numeroPos):
                    nuevasPos += R(posiciones[posicion],parametros[0],parametros[1])
                parametros[0] *= 2
            if comando is "B":
                for posicion in range(numeroPos):
                    nuevasPos += B(posiciones[posicion],parametros[0],parametros[1])
                parametros[1] *= 2
            if comando is "T":
                for posicion in range(numeroPos):
                    nuevasPos += T(posiciones[posicion],parametros[0],parametros[1])
                parametros[1] *= 2    

            posiciones = nuevasPos

            posiciones = list(OrderedDict.fromkeys(posiciones))
        
        posiciones.sort()
        printResult(posiciones)
        writeFile.write("Case #%i:\n" % caseNumber)
        for pos in posiciones:
            
            writeFile.write("%i %i\n" % (pos[0], pos[1]))

        
                              
            
