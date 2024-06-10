import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

# Create the main window
window = tk.Tk()
window.title("Copiar/Mover archivos")

# Increase column separation
window.grid_columnconfigure(0, minsize=300)
window.grid_columnconfigure(1, minsize=90)
window.grid_columnconfigure(2, minsize=90)

# Variables
input_dir = tk.StringVar()
output_dir = tk.StringVar()
move_files = tk.BooleanVar(value=False)
extension = tk.StringVar(value="pdb")
name_contains = tk.StringVar(value="rank_001")
name_startswith = tk.BooleanVar()

# Function to browse directory
def browse_directory(path_var):
    path_var.set(filedialog.askdirectory())

# Function to execute the move or copy
def execute():
    ext = extension.get()
    # If the extension starts with a period, remove it
    if ext.startswith("."):
        ext = ext[1:]

    input_directory = convertir_a_ruta_larga(input_dir.get())
    output_directory = convertir_a_ruta_larga(output_dir.get())

    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(ext) and (
                name_contains.get() in file if not name_startswith.get()
                else file.startswith(name_contains.get())
            ):
                file_path = convertir_a_ruta_larga(os.path.join(root, file))
                destination_path = convertir_a_ruta_larga(os.path.join(output_directory, file))
                if move_files.get():
                    shutil.move(file_path, destination_path)
                else:
                    shutil.copy(file_path, destination_path)
    messagebox.showinfo("Operación Finalizada", "El proceso ha finalizado.")

# Define layout
tk.Label(window, text="Selecciona el directorio de origen.").grid(row=0, column=0, sticky='W')
tk.Entry(window, textvariable=input_dir, width=60).grid(row=0, column=1)
tk.Button(window, text="Examinar", command=lambda: browse_directory(input_dir)).grid(row=0, column=2)

tk.Label(window, text="Selecciona el directorio de destino.").grid(row=1, column=0, sticky='W')
tk.Entry(window, textvariable=output_dir, width=60).grid(row=1, column=1)
tk.Button(window, text="Examinar", command=lambda: browse_directory(output_dir)).grid(row=1, column=2)

tk.Checkbutton(window, text="Marca esta casilla si deseas mover los ficheros en vez de copiarlos.", variable=move_files).grid(row=2, column=0, columnspan=3, sticky='W')

tk.Label(window, text="Indica la extensión de los ficheros que desea mover.").grid(row=3, column=0, sticky='W')
tk.Entry(window, textvariable=extension, width=60).grid(row=3, column=1)

tk.Label(window, text="Indica la expresión contenida en el nombre de los ficheros que desea mover.").grid(row=4, column=0, sticky='W')
tk.Entry(window, textvariable=name_contains, width=60).grid(row=4, column=1)

tk.Checkbutton(window, text="Marca esta casilla si los nombres de los ficheros deben empezar obligatoriamente por esta expresión.", variable=name_startswith).grid(row=5, column=0, columnspan=3, sticky='W')

tk.Button(window, text="Ejecutar", command=execute).grid(row=6, column=0, columnspan=3)

# Start the GUI loop
window.mainloop()
