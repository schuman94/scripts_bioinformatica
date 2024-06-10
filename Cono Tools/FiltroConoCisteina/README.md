# Filtrado de secuencias FASTA

Este programa permite filtrar secuencias en formato FASTA según diferentes criterios:

- Patrón "C": se filtran todas las secuencias que contengan un número específico de cisteínas, indicado por el usuario.
- Patrón "Patrón alfa": se filtran todas las secuencias que cumplan con el patrón alfa, pudiendo indicar el número de aminoácidos en cada uno de los dos gaps.

El resultado se guardará en un fichero fasta en el directorio seleccionado.

## Requisitos para ejecutar en Windows

Ejecutar el fichero .exe

## Requisitos para ejecutar desde consola

El programa requiere la instalación de Python 3 y las siguientes librerías:
- Biopython
- Tkinter

## Uso

1. Ejecutar el archivo `main.py` con Python 3 o el archivo .exe.
2. Seleccionar el archivo FASTA de entrada y la carpeta de salida.
3. Seleccionar el patrón de filtrado.
   - Para el patrón "C", indicar el número de cisteínas.
   - Para el patrón "Patrón alfa", indicar el número de aminoácidos en cada uno de los dos gaps.
4. Hacer clic en "Iniciar filtrado".

## Archivos

El programa consta de los siguientes archivos:
- `main.py`: archivo principal que contiene la interfaz gráfica y llama a las funciones necesarias.
- `file_utils.py`: archivo que contiene las funciones para seleccionar archivos y carpetas, así como la función para filtrar las secuencias.
- `filters.py`: archivo que contiene las funciones de filtrado.

## Compilación

Para compilar el programa en un archivo ejecutable de Windows, se puede utilizar la librería `pyinstaller` con el siguiente comando:
```sh
pyinstaller --onefile --noconsole main.py


Esto creará un archivo `main.exe` en la carpeta `dist/`.

## Autor

Este programa ha sido creado por Sergio Chulián Mantel.
