Este programa está diseñado para generar matrices comparativas entre péptidos, a partir de los resultados obtenidos en Rupee tras enfrentar una base de datos de péptidos consigo mismo.
Puede seleccionar fácilmente los directorios de entrada y salida para procesar los archivos y generar matrices basadas en distintos parámetros de evaluación.

Funcionalidades Clave:
Selección de Modo de Análisis: El usuario puede elegir entre tres modos diferentes para la generación de matrices:

RMSD (Root Mean Square Deviation): Utilizado para medir la diferencia entre posiciones de átomos correspondientes entre dos superposiciones de estructuras de proteínas.
Un valor proximo a cero indica un mayor parecido entre dos péptidos. Por defecto, cuando no haya comparación entre dos péptidos, su posición en la matriz quedará vacia, 
lo cual indica que Rupee ha considerado que no existe ningun parecido entre ambos péptidos.

TM-Score: Proporciona una medida de similitud entre dos estructuras de proteínas, normalizando respecto al tamaño de las proteínas. En esta ocasión, un mayor valor indica una mayor similutud.
Por el contrario, el valor por defecto cuando no hayan datos de similitud será cero.

Ratio: Calcula el cociente entre los valores RMSD y TM-Score para cada par de proteínas, ofreciendo una medida relativa de variación estructural.
Al igual que con RMSD, el valor por defecto cuando no hayan datos será una cadena vacía.

Generación Automatizada de Matrices: Al ejecutar el análisis, el programa procesa los archivos de datos y genera matrices que son almacenadas en formatos CSV y Excel, con etiquetas claras y formatos que facilitan su posterior análisis.
Notificaciones de Proceso Completado: Al finalizar la generación de la matriz, el usuario recibe una notificación informándole que el proceso ha concluido exitosamente y dónde encontrar los archivos generados.
