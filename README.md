# PrimesDB
[Inicio](README.md) | [Metadatos](METADATA.md) | [Capas de Abstracción](ABSTRACT.md) | [Ficheros](FILES.md) | [Acerca De](ABOUT.md)

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

bool función esPrimo (NúmeroComprobación)

    // Primero comprobamos los primeros primos
    Si NúmeroComprobación == (2, 3, 5, 7)
        Devuelve 1  // Es primo

    // Si no es el caso, extraemos el último dígito (en base 10)
    ÚltimoDígito = NúmeroComprobacion MODULO 10

    // Comprobamos si es par o múltiplo de 5. Esto se puede hacer de muchas maneras, pero en resumen:
    Si ÚltimoDígito == (0, 2, 4, 5, 6, 8)
        Devuelve 0  // No es primo

~~~

Esto nos deja con que tenemos que comprobar ***sólo los acabados en 1, 3, 7 y 9,*** por lo que aquí nos lleva a la base de funcionamiento de esta base de datos.

## Estructura de la Base de datos

Ya que sólo tendremos los primos en las terminaciones 1, 3, 7 y 9 los vamos a representar como las posiciones 0, 1, 2 y 3 de cada nibble. El nibble menos significativo almacenará las décadas impares y el nibble más significativo almacenará las pares.

Así por ejemplo, el primer byte de la base de datos contiene la comprobación computada de los números 11, 13, 17, 19, 21, 23, 27 y 29, almacenando un 1 para los primos y un 0 para los que no.

| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 29 | 27 | 23 | 21 | 19 | 17 | 13 | 11 |
| **1** | **0** | **1** | **0** | **1** | **1** | **1** | **1** |

**Hex:** 0xAF

El siguiente byte ya representará las décadas 30 y 40:

| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 49 | 47 | 43 | 41 | 39 | 37 | 33 | 31 |
| **0** | **1** | **1** | **1** | **0** | **1** | **0** | **1** |

**Hex:** 0x75

El tercer byte contendría las décadas 50 y 60, y así sucesivamente:

| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 69 | 67 | 63 | 61 | 59 | 57 | 53 | 51 |
| **0** | **1** | **0** | **1** | **1** | **0** | **1** | **0** |

**Hex:** 0x5A

Con esto se puede observar el poder de compresión de la información de este algoritmo específico para primos. En 3 bytes ya hemos almacenado el cómputo de 60 números.

## Cálculo de la dirección

La dirección como vemos, está directamente relacionada con el número que queremos representar o comprobar. Lo primero que debemos hacer es eliminar el dígito de las unidades (el que usamos para la comprobación inicial) truncándolo. Es decir, dividiendo por 10 e ignorando los decimales sin hacer una corrección ni al alza ni a la baja.

Ese valor almacenado representa la década que estamos calculando.

Ya que podemos representar 2 décadas por byte, el número resultante lo dividiremos entre 2.

Si ponemos el ejemplo del número 11 (el primer primo almacenado), al truncarlo después de dividirlo la década quedaría en 1, y al dividirlo por 2 quedaría como 0.5, por lo que debemos hacer 2 cosas.

Primero corregir el offset sumándole 0.5, por lo que la dirección en un principio queda como la posición 1 (lo cual es correcto desde el punto de vista humano), pero como tanto electrónica como computacionalmente empezamos desde la posición 0 debemos restarle 1 al resultado.

Pero si ponemos el ejemplo del número 21, Dirección => int(21/10)/2 = 1 + 0.5 = 1.5, o el ejemplo del 41 => 2.5

Debemos hacer una segunda corrección, por lo que después de sumarle el offset hay que truncar nuevamente los decimales.

Representamos en pseudocódigo la generación de la dirección:

~~~

    // Primero eliminamos las unidades, dividiendo entre 10 y truncando los decimales
    Década = int (NúmeroComprobación / 10)

    // Hacemos el cálculo de la dirección dividiendo entre 2, sumándole el offset,
    // truncando los decimales y restándole 1
    Dirección = int (Década / 2 + 0.5) - 1

~~~

## Cálculo del bit de posicionamiento

Por último, para acceder a cada bit según el número a comprobar, nos basamos en una tabla de sustitución que dará la posición del bit dentro del nibble y haremos un último ajuste, en este caso un offset a nivel de bit para seleccionar la década.

Pseudocódigo:

~~~

    Bits = {1, 3, 7, 9}

    //Localizamos la posición dentro del nibble
    Recorrer Bits
        Si Bits[x] == ÚltimoDígito
            Salir del Bucle

    //Si la década es par estamos en el 2º nibble, por lo que lo desplazamos 4 bits
    Si Década MODULO 2 == 0
        x = x + 4

~~~

Con esto ya tenemos completada tanto la dirección del byte como la posición del bit:

~~~

    Devolver FicheroBaseDatos(Dirección)[x]

~~~~

## Más Información

- [Capas de Abstracción](ABSTRACT.md)
- [Mapa de ficheros](FILES.md)
- [Acerca De](ABOUT.md)