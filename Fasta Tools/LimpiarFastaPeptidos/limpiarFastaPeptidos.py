import os
import re
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

def browse_file(entry):
    filepath = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta"), ("All files", "*.*")])
    entry.delete(0, END)
    entry.insert(END, filepath)

def browse_directory(entry):
    directory_path = filedialog.askdirectory()
    entry.delete(0, END)
    entry.insert(END, directory_path)

def filtrar_secuencias():
    archivo_fasta = convertir_a_ruta_larga(archivo_fasta_entry.get())
    archivo_salida = convertir_a_ruta_larga(os.path.join(directorio_entry.get(), 'Filtrado.fasta'))

    secuencias_filtradas = []
    descripciones_vistas = set()

    # Contadores
    total_secuencias = 0
    secuencias_descartadas = 0

    try:
        for record in SeqIO.parse(archivo_fasta, "fasta"):
            total_secuencias += 1

            # Filtro 1: Eliminar descripciones duplicadas
            if record.description in descripciones_vistas:
                secuencias_descartadas += 1
                continue
            descripciones_vistas.add(record.description)

            # Filtro 2: Eliminar secuencias vacías
            if len(record.seq) == 0:
                secuencias_descartadas += 1
                continue

            # Filtro 4: Eliminar secuencias con 'X'
            if 'X' in record.seq:
                secuencias_descartadas += 1
                continue

            # Filtro 5: Eliminar secuencias de ADN o ARN
            sequence = str(record.seq).upper()
            if re.match('^[ACGTU]*$', sequence):
                secuencias_descartadas += 1
                continue

            secuencias_filtradas.append(record)

        # Escribir secuencias filtradas al archivo de salida
        with open(archivo_salida, "w") as output_handle:
            SeqIO.write(secuencias_filtradas, output_handle, "fasta")

        messagebox.showinfo("Resultado", f"Total de secuencias originales: {total_secuencias}\n"
                                         f"Total de secuencias después de filtrar: {len(secuencias_filtradas)}\n"
                                         f"Total de secuencias descartadas: {secuencias_descartadas}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = Tk()
root.title("Filtrador de Secuencias FASTA")

archivo_fasta_label = Label(root, text="Archivo FASTA:")
archivo_fasta_label.grid(row=0, column=0, padx=5, pady=5)
archivo_fasta_entry = Entry(root, width=50)
archivo_fasta_entry.grid(row=0, column=1, padx=5, pady=5)
archivo_fasta_button = Button(root, text="Seleccionar", command=lambda: browse_file(archivo_fasta_entry))
archivo_fasta_button.grid(row=0, column=2, padx=5, pady=5)

directorio_label = Label(root, text="Directorio de Salida:")
directorio_label.grid(row=1, column=0, padx=5, pady=5)
directorio_entry = Entry(root, width=50)
directorio_entry.grid(row=1, column=1, padx=5, pady=5)
directorio_button = Button(root, text="Seleccionar", command=lambda: browse_directory(directorio_entry))
directorio_button.grid(row=1, column=2, padx=5, pady=5)

ejecutar_button = Button(root, text="Ejecutar", command=filtrar_secuencias)
ejecutar_button.grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
