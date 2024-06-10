Este programa es una herramienta interactiva diseñada para filtrar archivos en formato FASTA que contienen secuencias de aminoácidos.

Filtrado de Secuencias: El programa elimina secuencias basadas en varios criterios, incluyendo:
Eliminación de Descripciones Duplicadas: Secuencias con descripciones idénticas son eliminadas para evitar duplicados en el análisis.
Eliminación de Secuencias Vacías: Cualquier secuencia que esté vacía (sin datos) es descartada.
Eliminación de Secuencias con Caracteres 'X': Secuencias que contienen el carácter 'X', generalmente usado para indicar un residuo no especificado o desconocido, son eliminadas.
Exclusión de Secuencias que Contengan Solo Nucleótidos: El script filtra secuencias que contienen exclusivamente nucleótidos (A, C, G, T, U), indicando que pertenecen a ADN o ARN.

Interfaz Gráfica de Usuario permite:
Selección de Archivo FASTA: Los usuarios pueden seleccionar fácilmente el archivo FASTA desde su sistema a través de un diálogo de selección de archivos.
Selección de Directorio de Salida: Los usuarios eligen un directorio donde se guardarán las secuencias que pasen los filtros. Si el directorio no existe, se creará automáticamente.