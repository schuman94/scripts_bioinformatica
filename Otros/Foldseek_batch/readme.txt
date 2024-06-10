Guía de Usuario para la Aplicación de Búsqueda y Procesamiento de Proteínas con Foldseek
Introducción
Esta herramienta permite realizar búsquedas de estructuras de proteínas utilizando la API de Foldseek y procesar los resultados de manera automática.
La aplicación cuenta con una interfaz gráfica (GUI) que facilita la selección de archivos y la configuración de las opciones de búsqueda. Los resultados se descargan, formatean y guardan en archivos accesibles para su análisis posterior.


La aplicación permite:

Seleccionar un directorio que contiene archivos de proteínas en formato .pdb.
Seleccionar un directorio de salida donde se guardarán los resultados.
Elegir el modo de búsqueda (3diaa o tmalign).
Seleccionar la base de datos contra la cual se realizará la búsqueda (afdb-swissprot, afdb50, afdb-proteome).

Requisitos para ejecutarlo en Windows:
Ejecuta el fichero .exe

Requisitos para ejecutarlo desde Python:

Python 3.x instalado en el sistema.
Librerías necesarias: requests, pandas, tkinter.
Instalación de Dependencias
Puedes instalar las librerías necesarias ejecutando el siguiente comando en la terminal: pip install requests pandas tk


Uso de la Aplicación
Paso 1: Ejecutar la Aplicación
Ejecuta el archivo con doble click el archivo .exe o el archivo main.py en tu terminal: python main.py 

Paso 2: Interfaz Gráfica
Aparecerá una ventana con la interfaz gráfica de la aplicación.


Paso 3: Selección de Directorios
Input Directory (Directorio de Entrada): Haz clic en el botón "Browse..." junto a este campo para seleccionar el directorio que contiene los archivos .pdb que deseas procesar.
Output Directory (Directorio de Salida): Haz clic en el botón "Browse..." junto a este campo para seleccionar el directorio donde se guardarán los resultados.

Paso 4: Configuración de Opciones
Mode (Modo): Selecciona el modo de búsqueda entre 3diaa y tmalign.
Database (Base de Datos): Selecciona la base de datos contra la cual se realizará la búsqueda. Las opciones disponibles son afdb-swissprot, afdb50, afdb-proteome.
Paso 5: Ejecución
Haz clic en el botón "Execute" para iniciar el proceso.
La aplicación realizará las siguientes acciones por cada archivo .pdb en el directorio de entrada:
Iniciará una búsqueda en Foldseek.
Verificará el estado de la búsqueda hasta que se complete.
Descargará y procesará los resultados.
Los resultados se guardarán en el directorio de salida en formato .tsv y .xlsx.

Paso 6: Finalización
Una vez que el proceso haya terminado, aparecerá un mensaje informándote de que el proceso ha finalizado.

Conclusión
Esta herramienta proporciona una forma automatizada y eficiente de realizar búsquedas de estructuras de proteínas y procesar los resultados utilizando la API de Foldseek.
Con su interfaz gráfica, es accesible para usuarios sin experiencia en la línea de comandos, permitiendo una fácil configuración y ejecución del flujo de trabajo.

