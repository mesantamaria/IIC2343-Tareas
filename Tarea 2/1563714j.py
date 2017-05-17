import sys
Args = sys.argv
#data = open(Args[1], "r")
data = open("test2.txt", "r")
memoria = []
for a in range(0, 10):  # CREAR MEMORIA CON VALORES
    memoria.append(0)

A = 0
B = 0
data_list = []
direccion_list = []
instruccion_list = []
for linea in data:
    lista = linea.split()
    p = ""
    linea = p.join(lista)
    direccion_linea = ""
    instruccion_linea = ""
    if ":" in linea:
        i = 0
        while linea[i] != ":":
            direccion_linea += linea[i]
            i += 1
        i += 1
        while i < len(linea):
            instruccion_linea += linea[i]
            i += 1
    else:
        for letra in linea:
            instruccion_linea += letra
    direccion_list.append(direccion_linea)
    instruccion_list.append(instruccion_linea)
#print(direccion_list)
#print(instruccion_list)
data.close()

data_w = open("1563714j.txt", "w")
linea = 0
while linea < len(instruccion_list):
    instruccion = ""
    if ":" not in instruccion_list[linea]:
        i = 0 #contador
        if "OR" in instruccion_list[linea] and "XOR" not in instruccion_list[linea]:  # OR es unica instruccion con menos de 3 letras
            instruccion = "OR"
            i += 2
        else:
            while i < 3:
                if instruccion_list[linea][i] == " ":
                    break
                instruccion += instruccion_list[linea][i]
                i += 1
        operando1 = ""
        operando2 = ""
        direccion_destino_jump = ""
        while i < len(instruccion_list[linea]):
            if instruccion_list[linea][i] == "," or instruccion_list[linea][i] == "\n":
                break
            if "J" in instruccion_list[linea]:
                direccion_destino_jump += instruccion_list[linea][i]
                operando1 = "0"
                operando2 = "0"
            else:
                operando1 += instruccion_list[linea][i]
            i += 1
        i += 1
        while i < len(instruccion_list[linea]):
            if instruccion_list[linea][i] == " " or instruccion_list[linea][i] == "\n":
                break
            operando2 += instruccion_list[linea][i]
            i += 1
        if operando2 == "":
            operando2 = "0"
    #print("OPERANDO 1:", operando1, "OPERANDO 2:", operando2)
    d1 = False
    reg_A = False
    reg_B = False
    n1 = False # señal negativo
    n2 = False
    ####ACTIVAR SEÑALES PARA EL PRIMER OPERANDO
    if "(" in operando1: #verificar si es DIRECCION
        if "A" in operando1:
            direccion1 = A
        elif "B" in operando1:
            direccion1 =  B
        else:
            direccion1 = operando1[1:len(operando1) - 1]
            direccion1 = int(direccion1)
        d1 = True
        if direccion1 > len(memoria)-1 or memoria == []:
            memoria.append(0)
        else:
            operando1 = memoria[direccion1]
    elif "A" in operando1: # verificar si es REGISTRO
        operando1 = A
        reg_A = True
    elif "B" in operando1:
        operando1 = B
        reg_B = True


    #### OBTENER VALORES PARA OPERANDO 2
    if "(" in operando2:  # verificar si es DIRECCION
        if "A" in operando2:  # INDIRECTO
            direccion2 = A
        elif "B" in operando2:
            direccion2 =  B
        else:                 # DIRECTO
            direccion2 = operando2[1:len(operando2)-1]
            direccion2 = int(direccion2)
        d2 = True
        operando2 = memoria[direccion2]
    elif "A" in operando2: # verificar si es REGISTRO
        operando2 = A
    elif "B" in operando2:
        operando2 = B
    else:                  # LITERAL
        operando2 = int(operando2)

    # INSTRUCCIONES
    if instruccion == "MOV":
        if d1 == True:
            memoria[direccion1] = operando2
        elif reg_A == True:
            A = operando2
        elif reg_B == True:
            B = operando2
    elif instruccion == "ADD":
        if d1 == True:
            memoria[direccion1] = A + B
        elif reg_A == True:
            A += operando2
        elif reg_B == True:
            B += operando2
    elif instruccion == "SUB":
        if d1 == True:
            memoria[direccion1] = A - B
        elif reg_A == True:
            A -= operando2
        elif reg_B == True:
            B -= operando2
    elif instruccion == "INC":
        if d1 == True:
            memoria[direccion1] += 1
        elif reg_A == True:
            A += 1
        elif reg_B == True:
            B += 1

    if d1 == True:
        operando1 = memoria[direccion1]
    elif reg_A == True:
        operando1 = A
    elif reg_B == True:
        operando1 = B
###################################################### ZONA JUMP
    if instruccion == "CMP":
        comparacion = operando1 - operando2
    elif instruccion == "JMP":
        i = 0
        while i < len(direccion_list):
            if direccion_list[i] == direccion_destino_jump:
                linea = i-1  # se suma uno al final
                break
            i += 1
    elif instruccion == "JEQ":
        if comparacion == 0:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    linea = i - 1  # se suma uno al final
                    break
                i += 1
    elif instruccion == "JNE":
        if comparacion != 0:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    linea = i - 1  # se suma uno al final
                    break
                i += 1
    elif instruccion == "JGT":
        if comparacion > 0:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    linea = i - 1  # se suma uno al final
                    break
                i += 1
    elif instruccion == "JLT":
        if comparacion < 0:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    linea = i - 1  # se suma uno al final
                    break
                i += 1
    elif instruccion == "JGE":
        if comparacion >= 0:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    linea = i - 1  # se suma uno al final
                    break
                i += 1
    elif instruccion == "JLE":
        if comparacion <= 0:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    linea = i - 1  # se suma uno al final
                    break
                i += 1


##################### PASAR A BINARIO PARA AND OR NOT XOR
    if d1 == True:
        operando1 = A
        operando2 = B

    if int(operando1) < 0:
        n1 = True
        operando1 = str(operando1)[1:]
    if int(operando2) < 0:
        n2 = True
        operando2 = str(operando2)[1:]

    operando1 = bin(int(operando1))[2:len(bin(int(operando1)))]
    operando2 = bin(int(operando2))[2:len(bin(int(operando2)))]
    if len(operando1) < 8: # IGUALAR BITS
        diferencia = 8 - len(operando1)
        operando1 = "0" * diferencia + operando1
    elif len(operando1) > 8:
        diferencia = len(operando1) - 8
        operando1 = operando1[diferencia:]
    if len(operando2) < 8:
        diferencia = 8 - len(operando2)
        operando2 = "0" * diferencia + operando2
    elif len(operando2) > 8:
        diferencia = len(operando2) - 8
        operando2 = operando2[diferencia:]
    if n1 == True:
        complemento = ""
        for i in range(0, len(operando1)):
            if operando1[i] == "0":
                complemento += "1"
            else:
                complemento += "0"
        operando1 = bin(int(complemento, 2) + 1)[2:]
    if n2 == True:
        complemento = ""
        for i in range(0, len(operando2)):
            if operando2[i] == "0":
                complemento += "1"
            else:
                complemento += "0"
        operando2 = bin(int(complemento, 2) + 1)[2:]


    ################################################## ZONA AND OR NOT XOR Y SHIFT
    resultado = "0"
    if instruccion == "AND":
        resultado = ""
        for i in range(0, len(operando1)):
            if operando1[i] == operando2[i] == "1":
                resultado += "1"
            else:
                resultado += "0"

        #print("Resultado:", resultado)

    elif instruccion == "OR":
        resultado = ""
        for i in range(0, len(operando1)):
            if operando1[i] == operando2[i] == "0":
                resultado += "0"
            else:
                resultado += "1"
        #print("Resultado:", resultado)

    elif instruccion == "NOT":
        resultado = ""
        for i in range(0, len(operando1)):
            if d1 == False:

                if operando2[i] == "0":
                    resultado += "1"
                else:
                    resultado += "0"
            else:
                if operando1[i] == "0":
                    resultado += "1"
                else:
                    resultado += "0"
        #print("Resultado:", resultado)

    elif instruccion == "XOR":
        resultado = ""
        for i in range(0, len(operando1)):
            if operando1[i] == operando2[i]:
                resultado += "0"
            else:
                resultado += "1"
        #print("Resultado:", resultado)

    elif instruccion == "SHL":
        resultado = ""
        if d1 == False:
            resultado = operando2[1:] + "0"
        else:
            resultado = operando1[1:] + "0"
        #print("Resultado:", resultado)

    elif instruccion == "SHR":
        resultado = ""
        if d1 == False:
            resultado = "0" + operando2[:len(operando2)-1]
        else:
            resultado = "0" + operando1[:len(operando2) - 1]
        #print("Resultado:", resultado)

    if resultado[0] == "1":  # COMPLEMENTO A 2
        complemento = ""
        for i in range(0, len(resultado)):
            if resultado[i] == "1":
                complemento += "0"
            else:
                complemento += "1"
        resultado = (int(complemento, 2) + 1) * (-1)
    else:
        resultado = int(resultado, 2)

    if instruccion == "AND" or instruccion == "OR" or instruccion == "NOT" or instruccion == "XOR" \
            or instruccion == "SHR" or instruccion == "SHL":
        if d1 == True:
            memoria[direccion1] = resultado
        elif reg_A == True:
            A = resultado
        elif reg_B == True:
            B = resultado
    n_A = False
    n_B = False
    if A < 0:
        A = bin(A)[3:]
        n_A = True
        complemento = ""
        if len(A) < 8:
            dif = 8 - len(A)
            A = "0" * dif + A
        for bit in A:
            if bit == "0":
                complemento += "1"
            else:
                complemento += "0"
        A = int(complemento, 2) + 1
        A = bin(A)[2:]
    else:
        A = bin(A)[2:]
    if B < 0:
        B = bin(B)[3:]
        n_B = True
        complemento = ""
        if len(B) < 8:
            dif = 8 - len(B)
            B = "0" * dif + B
        for bit in B:
            if bit == "0":
                complemento += "1"
            else:
                complemento += "0"
        B = int(complemento, 2) + 1
        B = bin(B)[2:]
    else:
        B = bin(B)[2:]

    if len(str(A)) == 8:
        complemento = ""
        if str(A)[0] == "1":
            for bit in str(A):
                if bit == "0":
                    complemento += "1"
                else:
                    complemento += "0"
            A = -1* (int(complemento, 2) + 1)
        else:
            A = int(str(A), 2)
    else:
        A = int(A, 2)
    if len(str(B)) == 8:
        complemento = ""
        if str(B)[0] == "1":
            for bit in str(B):
                if bit == "0":
                    complemento += "1"
                else:
                    complemento += "0"
            B = -1 * (int(complemento, 2) + 1)
        else:
            B = int(str(B), 2)
    else:
        B = int(str(B), 2)



    linea += 1
    #print("A: ", A, "B: ", B, "Memoria: ", memoria)

data_w.write("A:  "+ str(A) +"\nB:  "+ str(B))
data_w.close()