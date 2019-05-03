import sys

def not_so_complex_hash(inputText):
    hash = bytearray(16)
    textBytes = bytearray()
    textBytes.extend(map(ord, inputText))
    for i in range(len(textBytes)):
        hash[i % 16] = (hash[i % 16] + textBytes[i]) % 256
    return hash

def separarInput(inputText):
    cadenas = inputText.split("------")
    cadena1 = cadenas[0]
    cadena2 = cadenas[1]
    return (cadena1,cadena2)

def generarExtra(originalText, modifyiedText):
    hashOriginal = list(not_so_complex_hash(originalText))
    hashModificada = list(not_so_complex_hash(modifyiedText))
    diference = [a_i - b_i for a_i, b_i in zip(hashOriginal, hashModificada)]
    shiftOrig = (len(separarInput(originalText)[0])+3)%16
    print(shiftOrig)
    hashModificada = hashModificada[shiftOrig:]+hashModificada[:shiftOrig]
    print(hashOriginal)
    print(hashModificada)
    
    listaClave = list(not_so_complex_hash("03W000000S0e0000Xzzwue08BzQz0Z0DzzzzzzRzzzzzez_zz"))
    listaClave = listaClave[shiftOrig:]+listaClave[:shiftOrig]
    print(listaClave)

    print(diference)


if __name__ == "__main__":
    readFile = open(sys.argv[1], "r")
    writeFile = open("out.txt", "w")

    numeroCasos = int(readFile.readline())
    for caso in range(1, numeroCasos+1):
        m = int(readFile.readline())
        original = ""
        for _ in range(m):
            original += readFile.readline().replace("\n", "").replace("\r","")
        
        modificadas = ""
        l = int(readFile.readline())
        for _ in range(l):
            modificadas += readFile.readline().replace("\n", "").replace("\r","")
        
        print("Case #%i\n" % caso)
        print(original)
        print(modificadas)
        generarExtra(original,modificadas)

