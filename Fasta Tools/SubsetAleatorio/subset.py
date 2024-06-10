import sys
import os
import random
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

def seleccionar_secuencias():
    archivo_fasta = convertir_a_ruta_larga(archivo_fasta_entry.get())
    numero_secuencias = int(numero_secuencias_entry.get())
    directorio = convertir_a_ruta_larga(directorio_entry.get())

    # Leer todas las secuencias del archivo FASTA
    secuencias = list(SeqIO.parse(archivo_fasta, 'fasta'))

    # Verificar que el número de secuencias solicitadas no excede el total de secuencias disponibles
    if numero_secuencias > len(secuencias):
        messagebox.showerror("Error", f"El número de secuencias solicitadas excede el total disponible: {len(secuencias)}")
        return

    # Seleccionar aleatoriamente secuencias
    secuencias_seleccionadas = random.sample(secuencias, numero_secuencias)

    # Asegurarse de que el directorio existe, si no, crearlo
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    # Escribir cada secuencia seleccionada a un archivo FASTA individual
    for secuencia in secuencias_seleccionadas:
        nombre_limpio = re.sub(r'[<>:"/\|?*\\]', '_', secuencia.id)
        archivo_salida = os.path.join(directorio, nombre_limpio + '.fasta')
        with open(archivo_salida, 'w') as salida:
            salida.write(f">{secuencia.description}\n")
            salida.write(f"{secuencia.seq}\n")

    messagebox.showinfo("Información", f"Se han escrito {numero_secuencias} secuencias aleatorias en el directorio {directorio}.")

# Funciones para abrir diálogos de selección de archivos y directorios
def abrir_archivo_fasta():
    archivo_fasta = filedialog.askopenfilename()
    archivo_fasta_entry.delete(0, END)  # Limpiar el contenido actual del cuadro de texto
    archivo_fasta_entry.insert(0, archivo_fasta)  # Insertar la ruta del archivo seleccionado

def seleccionar_directorio():
    directorio = filedialog.askdirectory()
    directorio_entry.delete(0, END)  # Limpiar el contenido actual del cuadro de texto
    directorio_entry.insert(0, directorio)  # Insertar la ruta del directorio seleccionado

# Crear la ventana principal
root = Tk()
root.title("Selector de Secuencias")

# Crear etiquetas
archivo_fasta_label = Label(root, text="Archivo FASTA")
archivo_fasta_label.grid(row=0, column=0)

numero_secuencias_label = Label(root, text="Número de Secuencias")
numero_secuencias_label.grid(row=1, column=0)

directorio_label = Label(root, text="Directorio de Salida")
directorio_label.grid(row=2, column=0)

# Crear cuadros de texto
archivo_fasta_entry = Entry(root, width=50)
archivo_fasta_entry.grid(row=0, column=1)

numero_secuencias_entry = Entry(root, width=50)
numero_secuencias_entry.grid(row=1, column=1)

directorio_entry = Entry(root, width=50)
directorio_entry.grid(row=2, column=1)

# Crear botones
archivo_fasta_button = Button(root, text="Seleccionar Archivo FASTA", command=abrir_archivo_fasta)
archivo_fasta_button.grid(row=0, column=2)

directorio_button = Button(root, text="Seleccionar Directorio", command=seleccionar_directorio)
directorio_button.grid(row=2, column=2)

ejecutar_button = Button(root, text="Ejecutar", command=seleccionar_secuencias)
ejecutar_button.grid(row=3, column=0, columnspan=3)

# Mantener la ventana abierta
root.mainloop()
