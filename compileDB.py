################################################################################################
# Programa que genera un archivo binario con los valores de los bits a 1 si la posición 
# corresponde a un número primo y 0 en caso de no serlo.
# Las variables rango_inicio y rango_final determinan la cantidad de números que va a comprender dicha bbdd.
# El archivo resultante '0000.pdb' es usado como tabla en el script 'checkPrime.py'
# Se omiten los 10 primeros números, todos los números pares y todos los números acabados en 5.
# De esta forma se optimiza en gran medida el tamaño del archivo y posteriormente la velocidad de comprobación.
# Se han seguido las pautas especificadas por ChuxMan en el siguiente repositorio:
#  https://github.com/pekesoft/PrimesDB
#
# by @as_informatico
# 03-11-2023
################################################################################################

import time

def criva_de_eratostenes(limite):
    primos = [True] * (limite + 1)
    primos[0] = primos[1] = False
    for i in range(2, int(limite**0.5) + 1):
        if primos[i]:
            for j in range(i*i, limite + 1, i):
                primos[j] = False
    return primos

def generar_archivo_binario(archivo, inicio, final):
    if inicio < 0 or final < inicio:
        print("Error: Rango no válido.")
        return

    limite = max(final, 11)  # Ajustamos el límite mínimo a 11 para incluir el 11

    primos = criva_de_eratostenes(limite)
    with open(archivo, 'wb') as file:
        byte = 0
        bit_posicion = 0
        for i in range(11, min(final + 1, len(primos))):
            # Descartar números pares
            if i % 2 == 0:
                continue
            # Descartar números terminados en 5
            if i % 10 == 5:
                continue

            es_primo = primos[i]
            if es_primo:
                byte |= (1 << bit_posicion)

            bit_posicion += 1
            if bit_posicion == 8:
                file.write(byte.to_bytes(1, byteorder='big'))
                byte = 0
                bit_posicion = 0

        if bit_posicion > 0:
            file.write(byte.to_bytes(1, byteorder='big'))

rango_inicio = 10
rango_final = 1342177280
archivo = f'0000.pdb'
tiempo_inicio = time.time()
generar_archivo_binario(archivo, rango_inicio, rango_final)
print(f"Archivo {archivo} generado exitosamente.")
tiempo_transcurrido = time.time() - tiempo_inicio
print(f'Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos.\n')
