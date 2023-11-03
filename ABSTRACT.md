# Capas de Abstracción
[Inicio](README.md) | [Capas de Abstracción](ABSTRACT.md) | [Ficheros](FILES.md) | [Acerca De](ABOUT.md)

## Introducción

## Búsquedas y bases de datos heurísticas

## Bloques por capa de abstracción

|Nivel|Tamaño de bloque|Tipo de datos|Números/byte|Números/bit|
|:--:|:--:|:--:|:--:|:--:|
|0|64Mb|Absolutos|20|1|
|1|8Mb|Relativos|160|20|
|2|1Mb|Relativos|1.280|160|
|3|128Kb|Relativos|10.240|1.280|
|4|16Kb|Relativos|81.920|10.240|
|5|2Kb|Relativos|655.360|81.920|
|6|256b|Relativos|5.242.880|655.360|
|7|32b|Relativos|41.943.040|5.242.880|
|8|4b|Relativos|335.544.320|41.943.040|
|9|-|Relativos|2.684.354.560|335.544.320|
|10|-|Relativos|21.474.836.484|2.684.354.560|
|n|Tamaño[n-1] / 8|Relativos|Num/Byte[n-1] * 8|Num/Byte[n-1]|

Nivel de cambio de capa de abstracción: cuando 8 bits (de la siguiente capa de abstracción) sean 0.

## Posibilidad de mejora