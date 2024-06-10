Este script está diseñado para analizar y filtrar secuencias peptídicas basadas en masas específicas proporcionadas por el usuario a través de un archivo.
El script calcula un rango de masa usando un valor de error dado y luego busca coincidencias en un conjunto de datos de secuencias, para finalmente generar un archivo Excel con los resultados del análisis.

Datos de Entrada
Archivo de Secuencias: Un archivo que contiene información detallada de péptidos, incluyendo nombre, masa monoisotópica, masa promedio, secuencia y modificaciones postraduccionales (PTMs).
Archivo de Masas: Un archivo de texto que lista las masas objetivo. Cada masa en este archivo es utilizada para crear un rango de búsqueda basado en el error especificado.
Parámetros de Usuario:
Tipo de Masa: El usuario debe seleccionar si desea utilizar la masa monoisotópica ('mass mono') o la masa promedio ('mass avg') para el análisis.
Corrección de Masa: Un valor numérico que se añadirá a cada masa de péptido durante el análisis para ajustar las mediciones.
Error: Un valor numérico que define el rango de tolerancia alrededor de cada masa objetivo; se usa para determinar qué secuencias están suficientemente cerca de la masa objetivo.
Datos de Salida
El script produce un archivo Excel que contiene las siguientes columnas:

Peak Mass: La masa objetivo del archivo de masas.
Peptide Mass: La masa del péptido que coincide dentro del rango especificado.
Mass Error: La diferencia absoluta entre la masa objetivo y la masa del péptido.
Peptide Name: El nombre del péptido, extraído del encabezado en el archivo de secuencias.
Peptide Sequence: La secuencia de aminoácidos del péptido.
Peptide PTMs: Las modificaciones postraduccionales asociadas con la secuencia.
Funcionamiento del Script
Selección de Archivos y Directorios: Utiliza una interfaz gráfica para seleccionar el archivo de secuencias, el archivo de masas y el directorio de salida.
Ingreso de Parámetros: El usuario debe especificar el tipo de masa, la corrección de masa y el valor de error.
Ejecución del Análisis: Una vez configurado todo, el usuario inicia el proceso. El script lee las masas del archivo de masas y, para cada masa, genera un rango basado en el valor de error. Luego, busca en el archivo de secuencias cualquier péptido cuya masa ajustada caiga dentro de ese rango.
Generación de Resultados: Los resultados se organizan y se guardan en un archivo Excel en el directorio especificado.

Ejemplo de uso:

El fichero de secuencias tendría este contenido:
>Bromocontryphan-S
GCPWEPWC
mass mono |  mass avg | sequence                  | PTMs
  974.341 |   975.100 | GCPWEPWC                  | 
 1018.330 |  1019.109 | GCPW(Gla)PWC              | Glu>Gla (x1)
 
>conopressin-S
CIIRNCPRG
mass mono |  mass avg | sequence       | PTMs
 1028.500 |  1029.242 | CIIRNCPRG      | 
 1044.495 |  1045.241 | CIIRNCORG      | Pro>Hyp (x1)

>Contryphan-S
GCPWEPWC
mass mono |  mass avg | sequence                  | PTMs
  974.341 |   975.100 | GCPWEPWC                  | 
 1018.330 |  1019.109 | GCPW(Gla)PWC              | Glu>Gla (x1)

El fichero de masas tendría este contenido:
974.3
1019.1
1047

Los datos que se introducen en la interfaz son:
Tipo de masa: mass mono
Corrección de masa: 0
Error: 1


El fichero excel que obtendría tendría esta información:
Peak mass	Peptide mass	Mass error	Peptide name	Peptide sequence	Peptide PTMs
974,3	974,341	0,041	Bromocontryphan-S	GCPWEPWC	
974,3	974,341	0,041	Contryphan-S	GCPWEPWC	
1019,1	1018,33	0,77	Bromocontryphan-S	GCPW(Gla)PWC	Glu>Gla (x1)
1019,1	1018,33	0,77	Contryphan-S	GCPW(Gla)PWC	Glu>Gla (x1)
