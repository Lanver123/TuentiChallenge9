import sys
import math

if __name__ == "__main__":
    readFile = open(sys.argv[1], "r")
    writeFile = open("out.txt", "w")
    readFile.readline()
    
    case = 1
    for line in readFile:
        valores = line.split()
        genteCon = int(valores[0])
        genteSin = int(valores[1])
        numeroTortillas = math.ceil(genteCon/2) + math.ceil(genteSin/2)
        output = "Case #%i: %i\n" % (case, numeroTortillas)
        print(output)
        writeFile.write(output)
        case +=1
    