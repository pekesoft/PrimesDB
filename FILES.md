# Estructura de ficheros y carpetas

## [README.md](README.md)

Documentación del algoritmo de generación y de acceso a la base de datos.

## [ABSTRACT.md](ABSTRACT.md)

Documentación de los ficheros de las capas de abstracción para bases de datos de primos muy grandes.

## FILES.md (este fichero)

Mapa y documentación de los distintos archivos y rutas de este repositorio.

## [ABOUT.md](ABOUT.md)

Créditos de análisis, diseño, desarrollo y computación de los cálculos de los primos.

## PrimesDB

    Es la carpeta que contiene los ficheros de la base de datos propiamente dicha en bloques de 64Mb (64x1024x1024=67.108.864 bytes). Los ficheros tienen extensión pdb (primesDB) y el nombre es un número secuencial de bloque para poder concatenar varios bloques. El nombre del fichero forma parte del cálculo de la dirección del número para números superiores a 1.342.177.280, que es el límite de números por cada 64Mb y del primer bloque.

## Samples

Carpeta con ejemplos del algoritmo implementado en distintos lenguajes de programación.

### Python

Los ejemplos de python han sido desarrollados por Jesús Pacheco - [@as_informatico](https://twitter.com/as_informatico) y forman parte del primer prototipo de la base de datos.

#### compileDB.py

    Programa que calcula los primos del primer bloque y genera el fichero de la base de datos.

#### checkPrime.py

    Programa para comprobar cualquier número dentro de la base de datos.