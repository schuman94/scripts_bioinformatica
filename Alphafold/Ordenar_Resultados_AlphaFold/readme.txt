
Este script proporciona una herramienta para organizar los archivos que se obtienen como resultado de ejecutar AlphaFold en lote, moviendo archivos relacionados a subdirectorios correspondientes.

Funcionalidad del Script:
Organización de Archivos: El script identifica y mueve archivos basados en un patrón de nombre específico dentro de un directorio dado. Busca subdirectorios que terminan con "_env" y mueve cualquier archivo en el directorio principal cuyo nombre base coincida con el nombre del subdirectorio (sin el sufijo "_env") a ese subdirectorio.

Operación del Script:
Interfaz de Usuario: Utiliza una interfaz gráfica de usuario para permitir al usuario seleccionar fácilmente el directorio de trabajo.

Selección de Directorio:
El usuario utiliza un botón de "Examinar" para seleccionar el directorio donde se encuentran los archivos y subdirectorios.

Proceso de Ordenación:
Una vez seleccionado el directorio, el usuario puede iniciar el proceso de ordenación con el botón "Ordenar".
El script verifica si el directorio existe para evitar errores.
Se ejecuta la función mover_ficheros, que organiza los archivos según los criterios mencionados.

Feedback al Usuario:
Una vez completado el proceso, se muestra un mensaje indicando el éxito de la operación.