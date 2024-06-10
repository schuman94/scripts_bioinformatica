Aplicación gráfica diseñada para procesar archivos de texto que se obtienen como resultado de Rupee. Es necesario su uso sobre los resultados de Ruppe para obtener un formato correcto.

Su objetivo principal es filtrar y validar estos archivos según ciertos criterios definidos por el usuario y generar archivos de salida filtrados en un directorio especificado.
Además, la herramienta mantiene un registro de los archivos considerados inválidos.

Si no se desea aplicar ningun filtro, no se debe rellenar los campos de Max rmsd y Min tm_score. Esto es equivalente a indicar un valor muy alto en Max rmsd (por ejemplo 99999) y 0 en Min tm_score.
En caso contrario:

Max rmsd: Ingrese el valor máximo permitido para el campo rmsd. Los registros con valores superiores serán excluidos.
Min tm_score: Ingrese el valor mínimo permitido para el campo tm_score. Los registros con valores inferiores serán excluidos.
Si desea ejecutar el modo de matriz de similitud, asegúrese de que estos campos estén vacíos.

Se debe indicar la ruta del directorio donde se encuentran los resultados de Rupee, el directorio donde se quiere guardar los nuevos resultados y el directorio donde guardar el fichero log con el registro de los datos inválidos.

El modo Similarity matrix no debe marcarse, a menos que se quiera procesar resultados de Rupee consistentes en enfrentar un conjunto de péptidos consigo mismo para obtener una matriz de similitud.