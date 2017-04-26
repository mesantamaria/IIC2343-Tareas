import sys  #para usar la linea de comandos

def decimal_binario(decimal):
    binario = ""
    mitad_decimal_entera = int(decimal) / 2
    while True:
        if mitad_decimal_entera == int(mitad_decimal_entera):
            binario = "0" + binario

        else:
            binario = "1" + binario
        if mitad_decimal_entera < 1:
            break
        mitad_decimal_entera = int(mitad_decimal_entera) / 2
    # print(binario)
    if decimal == int(decimal):
        return binario
    binario += "."
    doble_decimal_fraccionaria = (decimal - int(decimal)) * 2
    while True and doble_decimal_fraccionaria != 0:
        binario = binario + str(int(doble_decimal_fraccionaria))
        if doble_decimal_fraccionaria == 1:
            break
        doble_decimal_fraccionaria = (doble_decimal_fraccionaria - int(doble_decimal_fraccionaria)) * 2
    #print("BINARIO", binario)
    return binario


def flotante_decimal(signo_s, significante, signo_e, exponente,zero):
    #if float(significante) != 0
    if zero==False:
        significante = "1." + significante

    exponente = int(exponente, 2)  # pasarlo a decimal
    exponente = str(exponente)
    if signo_e == "1":
        exponente = "-" + exponente
    numero_binario = float(significante) * 10 ** int(exponente)
    #print(int(numero_binario))

    a = 1
    numero_decimal = 0
    for i in str("{:.10f}".format(numero_binario)):      #el cambio de formato es para no tener problemas con la
                                                         #notación cientifica e
        if i != ".":
            numero_decimal += 2 ** (len(str(int(numero_binario))) - a) * int(i)
            a += 1
    if signo_s == "1":
        numero_decimal = "-" + str(numero_decimal)
    numero_decimal = str(numero_decimal)
    #print("DECIMAL ES",float(numero_decimal))

    return numero_decimal


# flotante_decimal("1","","1","1")


def determinar_exponente(numero_binario):
    parte_entera = int(numero_binario)
    parte_fraccionaria = "{:.16f}".format(numero_binario - int(numero_binario))
    #print("fraccionaria", parte_fraccionaria)
    exponente = 0
    exponente += len(str(parte_entera)) - 1
    if parte_entera == 0 and float(parte_fraccionaria) != 0:  # lo segundo es para el caso especial del 0
        for a in range(2, len(str(parte_fraccionaria))):
            exponente -= 1
            if str(parte_fraccionaria)[a] == "1":
                break

    #print(exponente)
    return exponente


def normalizar(numero_binario, exponente):
    numero_normalizado = numero_binario * 10 ** (-exponente)
    #print(numero_normalizado)
    numero_normalizado = float(str(numero_normalizado)[0:len(str(numero_binario)) + 1])
    #print(numero_normalizado)
    return numero_normalizado


def determinar_significante(numero_binario_string):  # quitarle el 1 del comienzo y la coma
    # input debe estar en la forma cientifica normalizado (1,.....)
    numero_binario_string = numero_binario_string[2:len(numero_binario_string)]  # elimina el primer 1
    #print(numero_binario_string)
    return numero_binario_string


# normalizar(1.875, 0)
# num=9
# num_binario=decimal_binario(num)
# print(num_binario)
# exp_num=determinar_exponente(float(num_binario))
# print(exp_num)
# print("hola")
# num_normalizado=normalizar(float(num_binario),exp_num)
# determinar_significante(str(num_normalizado))


args = sys.argv

data = open(args[1], "r")  # args[1] es el archivo que se escribe en linea de comando
num_lineas = 0
archivo = open("1563714J.txt", "w")

for linea in data:
    if linea[0] == "-":
        signo_s = "1"
    else:
        signo_s = "0"
    numero = ""
    for i in linea:  # Obtener numero decimal del archivo(como string)
        if i == " ":
            break
        elif i != "-":
            numero += i
    significante = decimal_binario(float(numero)) # aun no normalizado ni eliminado el primer 1
    # print(str(float(significante)))
    zero=False
    if float(significante)==0:
        zero=True
    exponente = determinar_exponente(float(significante))
    significante = normalizar(float(significante), exponente)  # normalizado
    significante = determinar_significante(str(significante))  # eliminamos el primer 1 y la coma


    if str(exponente)[0] == "-":
        signo_e = "1"
        exponente = exponente * (-1)
    else:
        signo_e = "0"

    #print("RESPUESTA:   ", "Signo S =", signo_s, "Significante =", significante, "Signo exponente=",
    #      signo_e, "Exponente =", exponente)

    bits_s = ""
    bits_e = ""

    for a in range(0, len(linea)):  # Obtener cantidad de bits significante y exponente de archivo
        if linea[a] == " ":
            b = a + 1
            #print(b)
            while linea[b] != "," and "," in linea:
                bits_s += linea[b]
                b += 1
                #print("B ES",b, linea[b])
        if linea[a] == ",":
            b = a + 1
            while b < len(linea):
                bits_e += linea[b]
                b += 1
    bits_s = int(bits_s)
    bits_e = int(bits_e)

    exponente = decimal_binario(float(exponente))  # pasarlo a binario
    exponente = str(exponente)  # Ajustar exponente segun cantidad de bits

    if zero==True:
        significante="0"
    if len(significante) <= bits_s and len(exponente) <= bits_e:  # Ajustar segun cantidad de bits y obtener el nuevo decimal
        nuevo_decimal = flotante_decimal(signo_s, significante, signo_e, exponente,zero)
        diferencia = bits_s - len(significante)
        significante += "0" * diferencia
        diferencia = bits_e - len(exponente)
        exponente = diferencia * "0" + exponente

    elif len(significante) >= bits_s and len(exponente) <= bits_e:
        significante = significante[0:bits_s]
        nuevo_decimal = flotante_decimal(signo_s, significante, signo_e, exponente,zero)
        diferencia = bits_e - len(exponente)
        exponente = diferencia * "0" + exponente

    elif len(significante) <= bits_s and len(exponente) >= bits_e:
        exponente = exponente[0:bits_e]
        nuevo_decimal = flotante_decimal(signo_s, significante, signo_e, exponente,zero)
        diferencia = bits_s - len(significante)
        significante += "0" * diferencia
    elif len(significante) >= bits_s and len(exponente) >= bits_e:
        significante = significante[0:bits_s]
        exponente = exponente[0:bits_e]
        nuevo_decimal = flotante_decimal(signo_s, significante, signo_e, exponente,zero)
    else:
        nuevo_decimal = flotante_decimal(signo_s, significante, signo_e, exponente,zero)


    respuesta = signo_s + significante + signo_e + exponente
    #print(signo_s, significante, signo_e, exponente)
    archivo.write(respuesta + " " + nuevo_decimal + "\n")

data.close()
archivo.close()
# decimal_binario(float("0.5"))
# determinar_exponente(n)
# decimal_binario(n)
