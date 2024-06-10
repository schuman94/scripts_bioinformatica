Este script permite filtrar secuencias de un fichero fasta teniendo en cuenta dos criterios.

Longitud máxima de aminoácidos. En el nuevo fichero obtenido solo se encontrarán las secuencias con un numero de aminoacidos igual o menor al indicado.
Inicio del identificador. En el nuevo fichero obtenido no se encontrarán las secuencias cuyo identificador comience por la cadena de caracteres indicada. 
Por ejemplo, si la cadena es "gene:", en se descartarán todas las secuencias que empiecen por ">gene:" (nota que el signo ">" no hay que incluirlo).