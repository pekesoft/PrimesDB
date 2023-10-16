# PrimesDB
Base de datos de números primos para uso computacional

## Introducción

Esta base de datos ha sido diseñada para almacenar de forma simbólica listados completos de números primos computados. Es capaz de almacenar 20 números computados en un solo byte.

La base de datos es modular, puede ser truncada en cualquier punto o fusionada con otros bloques para adaptarlos a cualquier necesidad, tanto de software como de hardware. En principio los bloques base han sido diseñados de 64Mb porque es un tamaño razonable de una memoria flash SPI, por lo que puede ser utilizado para computación a nivel electrónico, pero desde luego también a nivel de software.

Por esta razón, y teniendo en cuenta que los bloques por defecto son de 64Mb y es capaz de almacenar 20 números computados por byte, en una base de datos de este tamaño podemos almacenar 1.342.177.280 números computados (64 x 1024 x 1024 x 20). De los cuales en el primer bloque más de 50 millones son primos. Una cantidad más que decente para cualquier calculadora o proceso computacional que lo requiera.

## El algoritmo de almacenamiento

Esta es una base de datos posicional. El número a comprobar es parte del cálculo que conforma la dirección (o ID de acceso).

### Premisa 1: Omisiones

Los primeros primos (2, 3, 5 y 7) son omitidos, por lo que la base de datos empieza en la primera y segunda década (del 10 al 29).

### Premisa 2: El último dígito

Es necesario extraer en un primer momento el último dígito. Este es vital para determinar en una primera criba los números que sabemos que no son primos (los pares y los múltiplos de 5) además de los primeros primos.

Pseudocódigo:

~~~

    //Primero comprobamos los primeros primos
    Si NúmeroComprobación == (2, 3, 5, 7)
        Devuelve 1

    //Si no es el caso, extraemos el último dígito (en base 10)
    ÚltimoDígito = NúmeroComprobacion MODULO 10

    //Comprobamos si es par o múltiplo de 5. Esto se puede hacer de muchas maneras, pero en resumen:
    Si ÚltimoNúmero == (0, 2, 4, 5, 6, 8)
        Devuelve 0

~~~

Esto nos deja con que tenemos que comprobar sólo los acabados en 1, 3, 7 y 9, por lo que aquí nos lleva a la base de funcionamiento de esta base de datos.