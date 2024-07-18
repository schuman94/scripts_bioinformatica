Este script recibe como entrada un directorio que contiene los ficheros csv resultantes de Rupee, es decir, un csv en donde la primera fila son los encabezados:
n,file_name,db_id,rmsd,tm_score,search_mode,search_type.

También recibe como entrada un excel con la anotación de familias farmacologicas (descargado de Uniprot).

El script procesa en un dataframe el fichero csv y crea una nueva columna (rmsd/tm_score) que es el resultado de dividir el valor de la columna rmsd entre la columna tm_score.
Una vez hecho con todas las filas, se escoge la fila cuyo valor rmsd/tm_score sea más cercano a 0, es decir, más pequeño (pero siempre debe ser numero positivo o 0).

De esa fila elegida, se obtiene file_name, db_id y rmsd/tm_score

Estos 3 valores se añaden como entrada a un nuevo excel, donde la primera columna es file_name, la segunda es db_id, la tercera es rsmd/tm_score.

Hay 3 columnas más, que son llamadas "pharmacological_family", "description" y "function".
Estas otras 3 columnas se obtienen gracias al excel que también se le ha pasado como entrada, de manera que en ese excel hay que buscar en la primera columna una coincidencia con nuestro db_id,
cuando lo encuentre, el valor de "pharmacological_family" corresponde con la novena columna.
El valor de "description" corresponde con la undecima columna y el valor de "function" corresponde con la duodecima columna.
