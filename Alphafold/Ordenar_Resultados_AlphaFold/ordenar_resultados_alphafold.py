import os
import shutil
import glob
import tkinter as tk
from tkinter import filedialog, messagebox

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def mover_ficheros(directorio):
    directorio = convertir_a_ruta_larga(directorio)
    # obtenemos todos los subdirectorios que terminen en '_env'
    subdirectorios = [d for d in os.listdir(directorio) if os.path.isdir(os.path.join(directorio, d)) and d.endswith('_env')]

    for subdir in subdirectorios:
        # extraemos el nombre base
        nombre_base = subdir[:-4]

        # obtenemos todos los ficheros que comiencen con el nombre base
        ficheros_asociados = glob.glob(os.path.join(directorio, nombre_base+'*'))

        for fichero in ficheros_asociados:
            fichero = convertir_a_ruta_larga(fichero)
            # obtenemos el nombre del fichero para evitar mover el directorio a sí mismo
            nombre_fichero = os.path.basename(fichero)

            if nombre_fichero != subdir:  # nos aseguramos de no mover el directorio a sí mismo
                destino = convertir_a_ruta_larga(os.path.join(directorio, subdir, nombre_fichero))
                shutil.move(fichero, destino)

def seleccionar_directorio(entry):
    directorio = filedialog.askdirectory()
    entry.delete(0, tk.END)  # borramos cualquier texto existente
    entry.insert(0, directorio)  # insertamos la ruta del directorio seleccionado

def ordenar():
    directorio = entry.get()
    if not os.path.isdir(directorio):
        messagebox.showerror('Error', 'El directorio seleccionado no existe')
        return
    mover_ficheros(directorio)
    messagebox.showinfo('Éxito', 'El proceso de ordenar los ficheros ha terminado')

root = tk.Tk()
root.title('Ordenador de Ficheros')

entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)

btn_examinar = tk.Button(root, text='Examinar', command=lambda: seleccionar_directorio(entry))
btn_examinar.pack(padx=10, pady=10)

btn_ordenar = tk.Button(root, text='Ordenar', command=ordenar)
btn_ordenar.pack(padx=10, pady=10)

root.mainloop()
