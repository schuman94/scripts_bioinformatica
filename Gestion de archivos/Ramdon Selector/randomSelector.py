import os
import random
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def browse_directory(entry):
    dir_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir_path)

def execute_copy(input_dir, output_dir, file_count):
    if not input_dir.get() or not output_dir.get() or not file_count.get():
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    input_dir_path = convertir_a_ruta_larga(input_dir.get())
    output_dir_path = convertir_a_ruta_larga(output_dir.get())

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    files = [f for f in os.listdir(input_dir_path) if os.path.isfile(os.path.join(input_dir_path, f))]

    if len(files) < int(file_count.get()):
        messagebox.showerror("Error", "El número indicado es mayor que el número de archivos disponibles.")
        return

    random_files = random.sample(files, int(file_count.get()))

    for file in random_files:
        shutil.copy(os.path.join(input_dir_path, file), output_dir_path)

    messagebox.showinfo("Success", "La copia de archivos se completó con éxito.")

root = tk.Tk()
root.title("Random Selector")

input_dir = tk.StringVar()
output_dir = tk.StringVar()
file_count = tk.StringVar()

tk.Label(root, text="Directorio de entrada:").grid(row=0, sticky="E")
tk.Entry(root, textvariable=input_dir, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: browse_directory(tk.Entry(root, textvariable=input_dir))).grid(row=0, column=2)

tk.Label(root, text="Directorio de salida:").grid(row=1, sticky="E")
tk.Entry(root, textvariable=output_dir, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: browse_directory(tk.Entry(root, textvariable=output_dir))).grid(row=1, column=2)

tk.Label(root, text="Número de archivos:").grid(row=2, sticky="E")
tk.Entry(root, textvariable=file_count, width=10).grid(row=2, column=1, sticky='W')

tk.Button(root, text="Copiar archivos", command=lambda: execute_copy(input_dir, output_dir, file_count)).grid(columnspan=3)

root.mainloop()
