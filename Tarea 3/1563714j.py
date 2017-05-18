import sys

def separar_instruccion(archivo):
    global direccion_list
    global instruccion_list
    direccion_list = []
    instruccion_list = []
    for linea in archivo:
        lista = linea.split()
        linea = "".join(lista)
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
    return instruccion_list, direccion_list

def pasar_a_binario(numero_decimal):
    if numero_decimal < 0:
        numero_decimal = str(numero_decimal)[1:]
        binario_sin_signo = bin(int(numero_decimal))[2:]
        binario_negado = ""
        if len(binario_sin_signo) < 8:
            diferencia = 8 - len(binario_sin_signo)
            binario_sin_signo = diferencia * "0" + binario_sin_signo
        elif len(binario_sin_signo) >= 8:
            diferencia = len(binario_sin_signo) - 8
            binario_sin_signo = binario_sin_signo[diferencia:]

        for bit in binario_sin_signo:
            if bit == "1":
                binario_negado += "0"
            else:
                binario_negado += "1"
        binario_con_signo = int(binario_negado, 2) + 1
        binario_con_signo = bin(binario_con_signo)[2:]
        if len(binario_con_signo) < 8:
            diferencia = 8 - len(binario_con_signo)
            binario_con_signo = diferencia * "0" + binario_con_signo

    else:
        binario_con_signo = bin(numero_decimal)[2:]
        if len(binario_con_signo) < 8:
            diferencia = 8 - len(binario_con_signo)
            binario_con_signo = diferencia * "0" + binario_con_signo
        else:
            diferencia = len(binario_con_signo) - 8
            binario_con_signo = binario_con_signo[diferencia:]

    return binario_con_signo  ## ES UN STRING!!

def pasar_a_decimal(string_binario):
    if string_binario[0] == "1":
        binario_negado = ""
        for i in range(0, len(string_binario)):
            if string_binario[i] == "0":
                binario_negado += "1"
            else:
                binario_negado += "0"
        decimal = int(binario_negado, 2) + 1  # Positivo
        decimal = decimal * (-1)
    else:
        decimal = int(string_binario, 2)
    return decimal

def verificar_NZ(resultado_ALU):
    global N
    global Z
    if resultado_ALU < 0:
        N = True
    else:
        N = False
    if resultado_ALU == 0:
        Z = True
    else:
        Z = False

    return N, Z

arg = sys.argv
data = open(arg[1], "r")
separar_instruccion(data)

instruccion_list = instruccion_list
direccion_list = direccion_list
#print(instruccion_list)
#print(direccion_list)
PC = 0
SP = 255
BP = 255
A = 0
B = 0
N = False  # SEÑAL
Z = False  # SEÑAL
memoria = []
for a in range(0, 256):  # CREAR MEMORIA CON VALORES
    memoria.append(0)

while PC < len(instruccion_list):
    #print("Registro A: ", A, "Registro B: ", B)
    instruccion = ""
    i = 0
    if "OR" in instruccion_list[PC] and "XOR" not in instruccion_list[PC]:
        instruccion = "OR"  # OR es unica instruccion con menos de 3 letras
        i += 2
    elif "CALL" in instruccion_list[PC]:
        instruccion = "CALL"  # CALL tiene 4 letras
        i+=4
    elif "PUSH" in instruccion_list[PC]:
        instruccion = "PUSH"  # PUSH tiene 4 letras
        i+=4
    else:
        while i < 3:
            instruccion += instruccion_list[PC][i]
            i += 1
    operando1 = ""
    operando2 = ""
    direccion_destino_jump = ""
    while i < len(instruccion_list[PC]):
        if instruccion_list[PC][i] == ",":
            break
        if "J" in instruccion_list[PC] or instruccion == "CALL":
            direccion_destino_jump += instruccion_list[PC][i]
            operando1 = "0"
            operando2 = "0"
        else:
            operando1 += instruccion_list[PC][i]
        i += 1
    i += 1
    while i < len(instruccion_list[PC]):
        operando2 += instruccion_list[PC][i]
        i += 1
    if operando1 == "":
        operando1 = "0"
    if operando2 == "":
        operando2 = "0"
    #print("Instruccion:", instruccion, "| OPERANDO 1:", operando1, "| OPERANDO 2:", operando2)

    ###  SEÑALES
    N = N
    Z = Z
    dir_1 = False
    dir_2 = False
    La = False
    Lb = False
    señalBP = False
    Lpc = False  # SEÑAL DE CARGA PC
    ### Activar señales
    if "(" in operando1: #verificar si es DIRECCION
        if "A" in operando1:
            direccion1 = A
        elif "B" in operando1:
            direccion1 =  B
        else:
            direccion1 = operando1[1:len(operando1) - 1]
            direccion1 = int(direccion1)
        dir_1 = True
        if direccion1 > len(memoria)-1 or memoria == []:
            memoria.append(0)
        else:
            operando1 = memoria[direccion1]
    elif "A" in operando1: # verificar si es REGISTRO
        operando1 = A
        La = True
    elif "B" in operando1 and "BP" not in operando1:
        operando1 = B
        Lb = True
    elif "BP" in operando1:
        operando1 = BP
        señalBP = True
    elif "SP" in operando1:
        operando1 = SP
    elif operando1 == "":
        operando1 = 0
    else:
        operando1 = int(operando1)

    if dir_1 == False:
        operando1_binario = pasar_a_binario(operando1)

    #### OBTENER VALORES PARA OPERANDO 2
    if "(" in operando2:  # verificar si es DIRECCION
        if "A" in operando2:  # INDIRECTO
            direccion2 = A
        elif "B" in operando2 and "BP" not in operando2:
            direccion2 = B
        else:  # DIRECTO
            direccion2 = operando2[1:len(operando2) - 1]
            direccion2 = int(direccion2)
        dir_2 = True
        operando2 = memoria[direccion2]
    elif "A" in operando2:  # verificar si es REGISTRO
        operando2 = A
    elif "B" in operando2 and "BP" not in operando2:
        operando2 = B
    elif "BP" in operando2:
        operando2 = BP
    elif "SP" in operando2:
        operando2 = SP
    else:  # LITERAL
        operando2 = int(operando2)
    if dir_2 == False:
        operando2_binario = pasar_a_binario(operando2)

    #print("Operando 1 bin: ", operando1, operando1_binario, "Operando 2 bin: ",operando2,  operando2_binario)

    # INSTRUCCIONES
    if instruccion == "MOV":
        if dir_1 == True:
            memoria[direccion1] = operando2
        elif La == True:
            A = operando2
        elif Lb == True:
            B = operando2
        elif señalBP == True:
            BP = operando2
        verificar_NZ(operando2)


    elif instruccion == "ADD":
        if dir_1 == True:
            memoria[direccion1] = A + B
            verificar_NZ(memoria[direccion1])
        elif La == True:
            A += operando2
            verificar_NZ(A)
        elif Lb == True:
            B += operando2
            verificar_NZ(B)
    elif instruccion == "SUB":
        if dir_1 == True:
            memoria[direccion1] = A - B
            verificar_NZ(A-B)
        elif La == True:
            A -= operando2
            verificar_NZ(A)
        elif Lb == True:
            B -= operando2
            verificar_NZ(B)
    elif instruccion == "INC":
        if Lb == True:
            B += 1
        verificar_NZ(B)
################################################## ZONA AND OR NOT XOR Y SHIFT
    resultado = "0"
    if instruccion == "AND":
        resultado = ""
        for i in range(0, len(operando1_binario)):
            if operando1_binario[i] == operando2_binario[i] == "1":
                resultado += "1"
            else:
                resultado += "0"
    elif instruccion == "OR":
        resultado = ""
        for i in range(0, len(operando1_binario)):
            if operando1_binario[i] == operando2_binario[i] == "0":
                resultado += "0"
            else:
                resultado += "1"
    elif instruccion == "NOT":
        resultado = ""
        for i in range(0, len(operando1_binario)):
            if dir_1 == False:

                if operando2_binario[i] == "0":
                    resultado += "1"
                else:
                    resultado += "0"
            else:
                if operando1_binario[i] == "0":
                    resultado += "1"
                else:
                    resultado += "0"
    elif instruccion == "XOR":
        resultado = ""
        for i in range(0, len(operando1_binario)):
            if operando1_binario[i] == operando2_binario[i]:
                resultado += "0"
            else:
                resultado += "1"
    elif instruccion == "SHL":
        resultado = ""
        if dir_1 == False:
            resultado = operando2_binario[1:] + "0"
        else:
            resultado = operando1_binario[1:] + "0"
    elif instruccion == "SHR":
        resultado = ""
        if dir_1 == False:
            resultado = "0" + operando2_binario[:len(operando2_binario)-1]
        else:
            resultado = "0" + operando1_binario[:len(operando2_binario) - 1]
    resultado_dec = pasar_a_decimal(resultado)
    #print("Resultado:", resultado, "Resultado decimal",resultado_dec, "\n")

    if instruccion == "AND" or instruccion == "OR" or instruccion == "NOT" or instruccion == "XOR" \
            or instruccion == "SHR" or instruccion == "SHL":
        if dir_1 == True:
            memoria[direccion1] = resultado_dec
        elif La == True:
            A = resultado_dec
        elif Lb == True:
            B = resultado_dec
        verificar_NZ(resultado_dec)

    ############  ZONA JUMP
    if instruccion == "CMP":
        comparacion = operando1 - operando2
        verificar_NZ(comparacion)
    elif instruccion == "JMP":
        i = 0
        while i < len(direccion_list):
            if direccion_list[i] == direccion_destino_jump:
                PC = i
                Lpc = True
                break
            i += 1
    elif instruccion == "JEQ":
        if Z == True:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    PC = i
                    Lpc = True
                    break
                i += 1
    elif instruccion == "JNE":
        if Z == False:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    PC = i
                    Lpc = True
                    break
                i += 1
    elif instruccion == "JGT":
        if N == False:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    PC = i
                    Lpc = True
                    break
                i += 1
    elif instruccion == "JLT":
        if N == True:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    PC = i
                    Lpc = True
                    break
                i += 1
    elif instruccion == "JGE":
        if N == False or Z == True:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    PC = i
                    Lpc = True
                    break
                i += 1
    elif instruccion == "JLE":
        if N == True or Z == True:
            i = 0
            while i < len(direccion_list):
                if direccion_list[i] == direccion_destino_jump:
                    PC = i # se suma uno al final
                    Lpc = True
                    break
                i += 1

    elif instruccion == "CALL":
        memoria[SP] = PC + 1
        SP -= 1
        i = 0
        while i < len(direccion_list):
            if direccion_list[i] == direccion_destino_jump:
                PC = i
                Lpc = True
                break
            i += 1

    elif instruccion == "RET":
        SP += 1
        PC = memoria[SP]
        Lpc = True
        if str(operando1) != "":
            SP += operando1

    elif instruccion == "PUSH":
        if La == True:
            memoria[SP] = A
        elif Lb == True:
            memoria[SP] = B
        elif señalBP == True:
            memoria[SP] = BP
        SP -= 1

    elif instruccion == "POP":
        SP += 1
        if La == True:
            A = memoria[SP]
        elif Lb == True:
            B = memoria[SP]
        elif señalBP == True:
            BP = memoria[SP]
    if A > 127 or A < -128:
        A = pasar_a_binario(A)  # Por si es mayor a 127
        A = pasar_a_decimal(A)
    if B > 127 or B < -128:
        B = pasar_a_binario(B)
        B = pasar_a_decimal(B)
    if BP < 0: # Solo datos entre 0 y 255
        BP = pasar_a_binario(BP)
        BP = int(BP, 2)
    #print("SP", SP, "BP", BP)
    if Lpc == False:
        PC += 1
#for elem in memoria:
 #   print(elem)
archivo = open("1563714j.txt", "w")
archivo.write("A: " + str(A) + "\nB: " + str(B) + "\nSP: " + str(SP) + "\nBP: " + str(BP))
print("Archivo: ", arg[1], "\n", "Registro A: ", A, "\n", "Registro B: ", B, "\n", "SP: ",
      SP, "\n", "BP: ", BP)
