# Capas de Abstracción
[Inicio](README.md) | [Metadatos](METADATA.md) | [Capas de Abstracción](ABSTRACT.md) | [Ficheros](FILES.md) | [Acerca De](ABOUT.md)

## Introducción

A medida que crezca la base de datos nos vamos a ir percatando de varias cosas, la primera es que en su mayoría estarán vacíos, y la segunda es que igualmente tenemos un límite físico que podemos alcanzar. Bien sea límite de RAM donde cargar la base de datos, límite de almacenamiento etc.

La base de datos al estar fragmentada es más manejable al menos en cuanto a terminos computacionales se refiere. No es lo mismo cargar un pequeño bloque de 64Mb que toda la base de datos al completo. Para ello vamos a crear unas capas de abstracción que nos permitirán acceder y almacenar números primos muy muy muy grandes. **Estas capas de abstracción no contienen primos como tal, si no un mapa de dónde se encuentran.**

Además el tamaño de bloque de 64Mb sólo es orientativo, como dijimos al principio se puede truncar o concatenar al tamaño que sea necesario para el fin específico que se esté usando o los límites que se quieran alcanzar, pero perfectamente si a medida que crece la base de datos va teniendo más y más ceros, no es necesario almacenarlos al tener esa información en las capas de abstracción, permitiendo hacer bloques más pequeños de hasta 8bytes, que sería el tamaño mínimo que se podría representar con las capas de abstracción.

## Búsquedas y bases de datos heurísticas

Las capas de abstracción son muy sencillas de generar y son progresivas. El algoritmo es el mismo para cualquier capa: Se recorre la base de datos que contiene los valores absolutos (la base de datos real) byte a byte. Si ese byte es igual a 0x00 (todos los bits a cero) en la capa de abstracción se fijará un 0, en cualquier otro caso se marcará un 1. Esto nos indica simplemente que en ese grupo de 8 bits hay algún primo.

Primer byte de la capa de abstracción 1. Cada bit representa un byte del nivel inferior (en este caso el 0, que tiene los valores absolutos)

| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 151-169 | 131-149 | 111-129 | 91-109 | 71-89 | 51-69 | 31-49 | 11-29 |
| **1** | **1** | **1** | **1** | **1** | **1** | **1** | **1** |

**Hex:** 0xFF

El siguiente byte ya representará las décadas del 171 al 329:

| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 311-329 | 291-309 | 271-289 | 251-269 | 231-249 | 211-229 | 191-209 | 171-189 |
| **1** | **1** | **1** | **1** | **1** | **1** | **1** | **1** |

**Hex:** 0xFF

Primeros 8 bytes calculados: FF FF FF FF FF FF 7F FE

La siguiente capa de abstracción (nivel 2) hará lo mismo que hemos hecho en el paso anterior, pero tomando como base a escanear el nivel anterior (en este caso el 1)

| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1131-1289 | 971-1129 | 811-969 | 651-809 | 491-649 | 331-489 | 171-329 | 11-169 |
| **1** | **1** | **1** | **1** | **1** | **1** | **1** | **1** |

**Hex:** 0xFF

Y así sucesivamente. A medida que vamos escalando en las capas de abstracción cada vez representa a grupos más grandes con un ratio de compresión 1:8 respecto a la capa anterior.

## Bloques por capa de abstracción

|Nivel|Tamaño de bloque|Tipo de datos|Números/byte|Números/bit|Ratio de compresión|
|:--:|:--:|:--:|:--:|:--:|:--:|
|0|64Mb|Absolutos|20|1|N/A|
|1|8Mb|Relativos|160|20|1:8|
|2|1Mb|Relativos|1.280|160|1:64|
|3|128Kb|Relativos|10.240|1.280|1:512|
|4|16Kb|Relativos|81.920|10.240|1:4.096|
|5|2Kb|Relativos|655.360|81.920|1:32.768|
|6|256b|Relativos|5.242.880|655.360|1:262.144|
|7|32b|Relativos|41.943.040|5.242.880|1:2.097.152|
|8|4b|Relativos|335.544.320|41.943.040|1:16.777.216|
|9|-|Relativos|2.684.354.560|335.544.320|1:134.217.728|
|10|-|Relativos|21.474.836.484|2.684.354.560|1:1.073.741.824|
|n|Tamaño[n-1] / 8|Relativos|Num/Byte[n-1] * 8|Num/Byte[n-1]|Ratio[n-1] * 8|

## Niveles superiores

## Posibilidad de mejora