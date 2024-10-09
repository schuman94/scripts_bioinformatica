import os
from tkinter import *
from tkinter import filedialog, messagebox
from Bio import SeqIO

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def browse_input_file(entry):
    filepath = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta"), ("All files", "*.*")])
    entry.delete(0, END)
    entry.insert(END, filepath)

def browse_output_directory(entry):
    directory_path = filedialog.askdirectory()
    entry.delete(0, END)
    entry.insert(END, directory_path)

def filtrar_secuencias_por_cadena():
    archivo_fasta = convertir_a_ruta_larga(archivo_fasta_entry.get())
    carpeta_salida = convertir_a_ruta_larga(carpeta_salida_entry.get())
    texto_busqueda = cadena_entry.get().strip()

    if not texto_busqueda:
        messagebox.showerror("Error", "El texto de búsqueda no puede estar vacío.")
        return

    # Generar el nombre del archivo de salida basado en El texto de búsqueda
    archivo_salida = os.path.join(carpeta_salida, f"{texto_busqueda}.fasta")

    secuencias_filtradas = []
    total_secuencias = 0
    secuencias_encontradas = 0

    try:
        # Leer el archivo FASTA
        for record in SeqIO.parse(archivo_fasta, "fasta"):
            total_secuencias += 1
            # Si El texto de búsqueda se encuentra en el identificador de la secuencia
            if texto_busqueda in record.description:
                secuencias_filtradas.append(record)
                secuencias_encontradas += 1

        # Escribir las secuencias filtradas al archivo de salida
        with open(archivo_salida, "w") as output_handle:
            SeqIO.write(secuencias_filtradas, output_handle, "fasta-2line")

        messagebox.showinfo("Resultado", f"Total de secuencias originales: {total_secuencias}\n"
                                         f"Secuencias encontradas: {secuencias_encontradas}\n"
                                         f"Archivo guardado en: {archivo_salida}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = Tk()
root.title("Filtrar Secuencias por Cadena en Identificador")

# Etiqueta y campo para seleccionar el archivo FASTA de entrada
archivo_fasta_label = Label(root, text="Archivo FASTA de entrada:")
archivo_fasta_label.grid(row=0, column=0, padx=5, pady=5)
archivo_fasta_entry = Entry(root, width=50)
archivo_fasta_entry.grid(row=0, column=1, padx=5, pady=5)
archivo_fasta_button = Button(root, text="Seleccionar", command=lambda: browse_input_file(archivo_fasta_entry))
archivo_fasta_button.grid(row=0, column=2, padx=5, pady=5)

# Etiqueta y campo para ingresar El texto de búsqueda
cadena_label = Label(root, text="texto de búsqueda:")
cadena_label.grid(row=1, column=0, padx=5, pady=5)
cadena_entry = Entry(root, width=50)
cadena_entry.grid(row=1, column=1, padx=5, pady=5)

# Etiqueta y campo para seleccionar la carpeta de salida
carpeta_salida_label = Label(root, text="Carpeta de salida:")
carpeta_salida_label.grid(row=2, column=0, padx=5, pady=5)
carpeta_salida_entry = Entry(root, width=50)
carpeta_salida_entry.grid(row=2, column=1, padx=5, pady=5)
carpeta_salida_button = Button(root, text="Seleccionar", command=lambda: browse_output_directory(carpeta_salida_entry))
carpeta_salida_button.grid(row=2, column=2, padx=5, pady=5)

# Botón para ejecutar el filtrado
ejecutar_button = Button(root, text="Filtrar y Guardar", command=filtrar_secuencias_por_cadena)
ejecutar_button.grid(row=3, column=1, padx=5, pady=10)

root.mainloop()
