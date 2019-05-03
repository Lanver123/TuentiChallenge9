import sys
import numpy as np
from fractions import Fraction

if __name__ == "__main__":
    readFile = open(sys.argv[1], "r")
    writeFile = open("out.txt", "w")

    numeroCasos = int(readFile.readline())
    casoMinimo = int(sys.argv[2])
    casoMaximo = int(sys.argv[3])
    
    for _ in range(casoMinimo-1):
        readFile.readline()
        readFile.readline()

    for caseNumber in range(casoMinimo, casoMaximo+1):
        numeroEntradas = int(readFile.readline())
        valores = readFile.readline().split()
        valores = list(map(int,valores))
        lcmVal = np.lcm.reduce(valores)

        newValores = [i * lcmVal for i in valores]
        sumaCaramelos = sum(newValores)
        numer = Fraction(sumaCaramelos,len(newValores)).numerator
        denom = Fraction(sumaCaramelos,len(newValores)).denominator
        print("Case #%i: %i/%i\n" % (caseNumber, numer, denom))
        writeFile.write("Case #%i: %i/%i\n" % (caseNumber, numer, denom))