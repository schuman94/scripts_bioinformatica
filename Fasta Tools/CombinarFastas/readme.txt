El script CombinarFastas.py es una herramienta diseñada para fusionar múltiples archivos en formato FASTA en un único archivo.

Funcionalidades del Script:
Interfaz Gráfica de Usuario (GUI): Utiliza tkinter para ofrecer una interfaz amigable que permite a los usuarios seleccionar fácilmente las carpetas de entrada y salida mediante botones de navegación.

Selección de Directorios:
Carpeta de Entrada: El usuario selecciona la carpeta que contiene los archivos FASTA que desea combinar.
Carpeta de Salida: El usuario elige la ubicación donde desea guardar el archivo FASTA combinado.

Ejecución del Proceso de Combinación:
Al ejecutar el proceso, el script busca todos los archivos con extensiones .fasta o .fa en la carpeta de entrada.
Lee cada archivo, procesa las secuencias y las combina en un único archivo. Durante este proceso, mantiene la integridad de las secuencias y sus encabezados correspondientes.
El archivo combinado se nombra utilizando el nombre de la carpeta de entrada y se guarda en la carpeta de salida especificada.

Manejo de Secuencias:
El script gestiona las secuencias de manera que todos los encabezados de secuencia (líneas que comienzan con >) se mantienen claramente separados en el archivo combinado.
Las secuencias asociadas a cada encabezado se escriben continuamente, eliminando cualquier salto de línea innecesario entre líneas de secuencia que pertenecen al mismo registro.

Notificaciones al Usuario:
Al finalizar el proceso, el programa notifica al usuario que la ejecución ha concluido correctamente, o en caso de error, muestra un mensaje explicativo.