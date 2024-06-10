El script permite a los usuarios descargar automáticamente archivos de modelos de proteínas desde AlphaFold usando identificadores de UniProt.
Las URLs para la descarga se construyen dinámicamente a partir de los identificadores proporcionados en un archivo de texto.

Toma la lista de identificadores y construye las URLs completas para la descarga de archivos PDB desde AlphaFold
La URL base para descargar modelos de AlphaFold es https://alphafold.ebi.ac.uk/files/AF-{identifier}-F1-model_v4.pdb.

Las descargas fallidas se registran en un archivo failed_downloads.txt en el directorio de destino.

Un ejemplo de fichero txt con una lista de IDs:

A0A0A0V633
A0A0A0V662
A0A0A0VBR5
A0A0A1I6E7