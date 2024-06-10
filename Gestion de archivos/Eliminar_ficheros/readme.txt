
Este script es una aplicación interactiva diseñada para eliminar archivos específicos dentro de un directorio basándose en nombres listados en un archivo de texto.

El usuario puede seleccionar un archivo de texto que lista los nombres de archivos (SIN LA EXTENSION) que se desean eliminar.
El usuario elige un directorio donde el script buscará los archivos mencionados en el archivo de texto.

Al ejecutar el proceso de eliminación, el script lee los nombres de los archivos desde el archivo de texto seleccionado.
Busca cada archivo en el directorio especificado. Si un archivo con un nombre que contiene alguna de las entradas del archivo de texto existe, lo elimina.
La operación es robusta frente a errores, y cualquier problema durante la eliminación (como permisos insuficientes) es manejado sin detener todo el proceso.
Una vez completado, se muestra un mensaje con el total de archivos eliminados.

Importante recordar que el fichero txt debe contener en cada linea el nombre de un fichero sin su extensión.
Por ejemplo, si se desea eliminar los ficheros A0A0A1I6E7.pdb y A0A0B4J2D5.pdb, en el txt aparecerá de la siguiente forma:

A0A0A1I6E7
A0A0B4J2D5

