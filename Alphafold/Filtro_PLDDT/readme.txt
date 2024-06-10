El script filtro_plddt es una herramienta diseñada para filtrar y organizar archivos de proteínas basados en el valor de calidad PLDDT obtenido a través de modelos computacionales como AlphaFold.
A continuación, te detallo su propósito y funcionalidad:

Propósito del Script:
El script permite al usuario filtrar archivos de proteínas (.pdb) según un valor umbral de PLDDT especificado.
El PLDDT es una métrica que indica la confianza en la precisión estructural de la proteína predicha. Los archivos de proteínas que superan este umbral se consideran de alta calidad y son copiados a una carpeta de salida para su posterior análisis o uso.

Funcionalidad del Script:
Interfaz Gráfica: El script utiliza una interfaz gráfica de usuario (GUI) para facilitar la interacción con el usuario, permitiendo seleccionar carpetas y establecer el valor del filtro de manera intuitiva.

Selección de Carpetas:
Carpeta de Entrada: El usuario selecciona una carpeta que contiene subcarpetas con los archivos JSON con los datos PLDDT de las proteínas.
Carpeta de Salida: Se selecciona una carpeta donde los archivos de proteínas que superen el filtro serán copiados.
Establecimiento del Valor del Filtro: El usuario puede ingresar un valor numérico que será usado como el umbral para filtrar los archivos de proteínas. Por defecto, este valor está configurado en 69.5.

Proceso de Filtrado:
El script recorre todos los archivos JSON en la carpeta de entrada, calculando el valor medio de PLDDT para cada proteína.
Si el valor medio de PLDDT de una proteína supera el umbral establecido, el archivo correspondiente de la proteína (.pdb) es copiado a la carpeta de salida.
Se genera un registro en formato CSV en una subcarpeta 'log' dentro de la carpeta de salida, documentando el nombre de cada proteína, su valor PLDDT medio, y si pasó o no el filtro.
Reporte de Errores y Resultados: Si alguna subcarpeta no contiene los archivos JSON esperados, se documenta en un archivo CSV de errores. Al finalizar el proceso, se muestra un mensaje indicando cuántas proteínas han pasado el filtro y se sugiere revisar la consola para más detalles.