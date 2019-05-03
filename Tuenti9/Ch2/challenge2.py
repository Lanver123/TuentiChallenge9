import sys
import math
import re

def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    
    if start not in graph:
        return

    for next in graph[start] - set(path):
        yield from dfs_paths(graph, next, goal, path + [next])

if __name__ == "__main__":
    readFile = open(sys.argv[1], "r")
    writeFile = open("out.txt", "w")

    numeroCasos = int(readFile.readline())
    for caseNumber in range(1, numeroCasos+1):
        grafo = {}

        #Construir grafo
        numeroConexiones = int(readFile.readline())
        for conexionI in range(1, numeroConexiones+1):
            nextLine = readFile.readline()
            aristas = re.split((":|,"), nextLine.replace("\n",""))
            grafo[aristas[0]] = set(aristas[1:])

        #Calcular numero maximo caminos
        numeroMaxCasos = len(list(dfs_paths(grafo, 'Galactica', 'New Earth')))  
        toPrint = "Case #%i: %i\n" % (caseNumber, numeroMaxCasos)
        print(toPrint)
        writeFile.write(toPrint)



    