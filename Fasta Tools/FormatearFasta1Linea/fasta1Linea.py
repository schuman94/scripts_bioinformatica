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

# Función para convertir FASTA
def convertir_fasta():
    archivo_entrada = convertir_a_ruta_larga(archivo_fasta_entry.get())
    directorio_salida = convertir_a_ruta_larga(directorio_entry.get())
    archivo_salida = convertir_a_ruta_larga(os.path.join(directorio_salida, "secuencia_una_linea.fasta"))

    try:
        with open(archivo_salida, "w") as salida:
            for registro in SeqIO.parse(archivo_entrada, "fasta"):
                salida.write(f">{registro.description}\n")
                salida.write(f"{str(registro.seq)}\n")
        messagebox.showinfo("Éxito", f"Archivo convertido exitosamente y guardado en {archivo_salida}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Función para seleccionar archivo FASTA
def abrir_archivo_fasta():
    archivo_fasta = filedialog.askopenfilename()
    archivo_fasta_entry.delete(0, END)
    archivo_fasta_entry.insert(0, archivo_fasta)

# Función para seleccionar directorio de salida
def seleccionar_directorio():
    directorio = filedialog.askdirectory()
    directorio_entry.delete(0, END)
    directorio_entry.insert(0, directorio)

# Crear ventana principal
root = Tk()
root.title("Convertidor de FASTA")

# Etiquetas
Label(root, text="Archivo FASTA").grid(row=0, column=0, sticky=W)
Label(root, text="Directorio de Salida").grid(row=1, column=0, sticky=W)

# Entradas
archivo_fasta_entry = Entry(root, width=50)
archivo_fasta_entry.grid(row=0, column=1)
directorio_entry = Entry(root, width=50)
directorio_entry.grid(row=1, column=1)

# Botones
Button(root, text="Abrir", command=abrir_archivo_fasta).grid(row=0, column=2)
Button(root, text="Seleccionar", command=seleccionar_directorio).grid(row=1, column=2)
Button(root, text="Convertir", command=convertir_fasta).grid(row=2, column=0, columnspan=3)

# Mantener la ventana abierta
root.mainloop()
