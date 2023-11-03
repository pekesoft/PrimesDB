#######################################################################################################
# Programa que comprueba si el número introducido es primo.
# El valor máximo comprobable es 1.342.177.280
# El valor máximo es el del archivo binario usado como tabla de verificación '0000.pdb'.
# El resultado es instantáneo.
# Se han seguido las pautas especificadas por ChuxMan en el siguiente repositorio:
#  https://github.com/pekesoft/PrimesDB
#
# by @as_informatico
# 03-11-2023
######################################################################################################

def esPrimoBaseDatos(numero_comprobacion, base_datos):
    if numero_comprobacion in (2, 3, 5, 7):
        return True  # Es primo

    ultimo_digito = numero_comprobacion % 10
    if ultimo_digito in (0, 2, 4, 5, 6, 8):
        return False  # No es primo

    decada = numero_comprobacion // 10
    direccion = int(decada / 2 + 0.5) - 1

    bits = {1: 0, 3: 1, 7: 2, 9: 3}
    posicion_bit = bits[ultimo_digito]
    if decada % 2 == 0:
        posicion_bit += 4

    byte = base_datos[direccion]
    bit_valor = (byte >> posicion_bit) & 1
    return bit_valor == 1

with open('0000.pdb', 'rb') as file:
    base_datos = file.read()

while True:
    try:
        while True:
            numero_a_comprobar = int(input("Ingrese el número que desea comprobar: "))
            if numero_a_comprobar > 1342177280:
                print("Introduzca un número igual o menor de 1342177280")
                break
            resultado = esPrimoBaseDatos(numero_a_comprobar, base_datos)
            if resultado:
                print(f"{numero_a_comprobar} ES PRIMO")
            else:
                print(f"{numero_a_comprobar} no es primo")

    except ValueError:
        print("Finalizando el programa")
        break
