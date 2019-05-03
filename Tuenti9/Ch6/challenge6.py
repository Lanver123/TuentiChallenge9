import sys
import networkx as nx
import matplotlib.pyplot as plt

def determineConections(palabras, DG):
    orden = []
    dict = {}
    for palabra in palabras:
        orden += [palabra[0]]
        dict.setdefault(palabra[0],[]).append(palabra[1:])

    for i in range(len(orden)-1):
        if orden[i+1] == orden[i]:
            continue
        DG.add_edge(orden[i], orden[i+1])

    for key in dict.keys():
        if len(dict[key]) > 1:
            valoresNuevos = []
            for valor in dict[key]:
                if valor != "":
                    valoresNuevos+=[valor]
            determineConections(valoresNuevos, DG)


    
if __name__ == "__main__":
    readFile = open(sys.argv[1], "r")
    writeFile = open("out.txt", "w")

    numeroCasos = int(readFile.readline())
    for caso in range(1, numeroCasos+1):
        DG = nx.DiGraph()        
        numeroPalabras = int(readFile.readline())        
        palabras = []
        for _ in range(numeroPalabras):
            palabras.append(readFile.readline().replace("\n",""))
        
        flat_list = [item for sublist in palabras for item in sublist]
        letras = list(set(flat_list).union(""))

        for letra in letras:
            DG.add_node(letra)

        determineConections(palabras,DG)

        leaves=[node for node in DG.nodes if DG.out_degree(node) == 0]
        roots=[node for node in DG.nodes if DG.in_degree(node) == 0]
        writeFile.write("Case #%i:" % caso)
        if len(roots) == 1 and len(leaves) == 1 and nx.dag_longest_path_length(DG)+1 == len(DG.nodes):
            for node in nx.dag_longest_path(DG):
                writeFile.write((" "+ node))
            writeFile.write("\n")
        else:
            writeFile.write(" AMBIGUOUS\n")

        nx.draw_circular(DG)
        plt.show()
                      