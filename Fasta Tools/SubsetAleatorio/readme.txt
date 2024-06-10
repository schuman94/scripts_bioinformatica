Este script es una herramienta interactiva diseñada para seleccionar un número específico de secuencias de ADN o proteínas de manera aleatoria desde un archivo FASTA y guardar cada secuencia seleccionada en un archivo FASTA separado dentro de un directorio especificado. El proceso se gestiona a través de una interfaz gráfica de usuario (GUI) basada en Tkinter, facilitando la selección de archivos y la configuración de opciones. Aquí te explico el funcionamiento y las características del script:

Funcionalidad del Script
Selección de Archivo FASTA: El usuario puede seleccionar un archivo FASTA desde su sistema de archivos, que contiene múltiples secuencias que podrían ser de ADN o proteínas. Esto se hace utilizando un diálogo de selección de archivos.
Ingreso del Número de Secuencias a Seleccionar: El usuario debe especificar cuántas secuencias desea extraer del archivo FASTA. Este número no debe exceder el total de secuencias disponibles en el archivo.
Selección de Directorio de Salida: El usuario escoge un directorio donde las secuencias seleccionadas serán guardadas en archivos FASTA individuales. Si el directorio no existe, el script lo creará.
Proceso de Selección y Guardado:
El script lee todas las secuencias del archivo FASTA.
Verifica que el número de secuencias a seleccionar no exceda el número de secuencias disponibles en el archivo.
Selecciona aleatoriamente el número especificado de secuencias.
Guarda cada secuencia en un archivo FASTA individual en el directorio especificado. Los nombres de los archivos se generan a partir del ID de cada secuencia, asegurándose de limpiar los caracteres no permitidos en nombres de archivos.