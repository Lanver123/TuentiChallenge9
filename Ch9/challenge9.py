 #!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from itertools import permutations

NUMS = ((1, u"一"),
        (2, u"二"),
        (3, u"三"),
        (4, u"四"),
        (5, u"五"),
        (6, u"六"),
        (7, u"七"),
        (8, u"八"),
        (9, u"九"),
        (10, u"十"),
        (100, u"百"),
        (1000, u"千"),
        (10000, u"万"))

KANJIS = dict((kanji, num) for (num, kanji) in NUMS)

class ContinueI(Exception):
    pass

def numerosPosibles(kanji, numeros, magnitudes):
    magnitudes.sort(reverse=True)
    magnitudes += [1]
    numeros += [0]*(len(magnitudes)-len(numeros))
    permutaciones = list(permutations(numeros))

    combinaciones = [list(zip(list(permutacion),magnitudes)) for permutacion in permutaciones]
    
    combinacionesFinales = []
    for combinacion in combinaciones:
        flag = False
        #Descartas los que tienen 1's sin sentido
        for tupla in combinacion:
            if tupla[1] == 1000 and tupla[0] == 1:
                flag = True
                break
            if tupla[1] == 100 and tupla[0] == 1:
                flag = True
                break
            if tupla[1] == 10 and tupla[0] == 1:
                flag = True
                break
        if not flag:
            #Cambias los 0's por 1's
            for tupla in combinacion:
                if tupla[1] == 10000 and tupla[0] == 0:
                    combinacion[combinacion.index(tupla)] = (1, tupla[1])
                if tupla[1] == 1000 and tupla[0] == 0:
                    combinacion[combinacion.index(tupla)] = (1, tupla[1])
                if tupla[1] == 100 and tupla[0] == 0:
                    combinacion[combinacion.index(tupla)] = (1, tupla[1])
                if tupla[1] == 10 and tupla[0] == 0:
                    combinacion[combinacion.index(tupla)] = (1, tupla[1])

        #Si tenemos un 1 * 1000 y un unico 1 en la pool, el numero no puede acabar en 1
        if 10000 in magnitudes and combinacion[0][0] == 1 and numeros.count(1) == 1 and combinacion[-1][0] == 1:
            continue
        if not flag:
            valorFinal = 0
            for tupla in combinacion:
                valorFinal += tupla[0]*tupla[1]

            combinacionesFinales += [valorFinal]
            
    return combinacionesFinales

def numberMagnitude(kanji):
    words = [word for word in kanji]
    magnitudes = []
    if u"万" in words:
        magnitudes += [10000]
    if u"千" in words:
        magnitudes += [1000]
    if u"百" in words:
        magnitudes += [100]
    if u"十" in words:
        magnitudes += [10]
    
    return magnitudes

def posibleNumbers(kanji):
    words = [word for word in kanji]
    numbers = []
    exponentials = (u"万", u"千", u"百", u"十")
    for word in words:
        if word not in exponentials:
            numbers += [KANJIS[word]]
    return numbers

def _break_down_nums(nums):
    first, second, third, rest = nums[0], nums[1], nums[2], nums[3:]
    if first < third or third < second:
        return [first+second, third] + rest
    else:
        return [first, second*third] + rest

def kanji2num(kanji, enc="utf-8"):
    """
    Convert the kanji number to a Python integer.
    Supply `kanji` as a unicode string, or a byte string
    with the encoding specified in `enc`.
    """
    if not isinstance(kanji, str):
        kanji = str(kanji, enc)

    # get the string as list of numbers
    nums = [KANJIS[x] for x in kanji]

    num = 0
    while len(nums) > 1:
        first, second, rest = nums[0], nums[1], nums[2:]
        if second < first: # e.g. [10, 3, …]
            if any(x > first for x in rest): # e.g. [500, 3, 10000, …]
                nums = _break_down_nums(nums)
            else: # e.g. [500, 3, 10, …]
                num += first
                nums = [second] + rest
        else: # e.g. [3, 10, …]
            nums = [first*second] + rest

    return num + sum(nums)

if __name__ == "__main__":
    continue_i = ContinueI()
    file = open(sys.argv[1],"r")
    writeFile = open("out.txt", "w")

    primerElems = []
    segundElems = []
    igualdades = []

    numberEquations = int(file.readline())
    case = 1
    for line in file:
        partes = line.split("OPERATOR")
        partes2 = partes[1].split("=")

        eq1 = partes[0].replace(" ","").replace("\n","")
        eq2 = partes2[0].replace(" ","").replace("\n","")
        igualdad = partes2[1].replace(" ","").replace("\n","")

        mag1 = numberMagnitude(eq1)
        mag2 = numberMagnitude(eq2)
        mag3 = numberMagnitude(igualdad)
        
        posible1 = posibleNumbers(eq1)
        posible2 = posibleNumbers(eq2)
        posible3 = posibleNumbers(igualdad)

        combinaciones1 = numerosPosibles(eq1,posible1,mag1)
        combinaciones2 = numerosPosibles(eq2, posible2,mag2)
        combinaciones3 = numerosPosibles(igualdad, posible3,mag3)
        resultado = []
        for combinacion1 in combinaciones1:
            try:
                for combinacion2 in combinaciones2:
                    for combinacion3 in combinaciones3:
                        saltar = False
                        if(combinacion1 + combinacion2 == combinacion3):
                            resultado += ["%i + %i = %i" % (combinacion1, combinacion2, combinacion3)]
                            saltar = True
                        elif(combinacion1 - combinacion2 == combinacion3):
                            resultado += ["%i - %i = %i" % (combinacion1, combinacion2, combinacion3)]
                            saltar = True
                        elif(combinacion1 * combinacion2 == combinacion3):
                            resultado += ["%i * %i = %i" % (combinacion1, combinacion2, combinacion3)]
                            saltar = True
                        if saltar:
                            combinaciones2.remove(combinacion2)
                            combinaciones3.remove(combinacion3)
                            raise continue_i
            except ContinueI:
                continue                   
        writeFile.write("Case #%i: " % (case) + resultado[0] + "\n")
        case +=1