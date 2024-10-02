import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
import pandas as pd

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def browse_file(entry):
    filepath = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(tk.END, filepath)

def browse_directory(entry):
    directory_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(tk.END, directory_path)

def filter_sequences():
    mass_type_input = mass_type.get()
    mass_correction = int(mass_correction_menu.get())
    error = float(error_entry.get())
    file_path = convertir_a_ruta_larga(file_entry.get())
    mass_file_path = convertir_a_ruta_larga(mass_file_entry.get())
    output_dir = convertir_a_ruta_larga(dir_entry.get())

    # Obtener el índice de la columna de masas especificado por el usuario
    try:
        mass_column_index = int(mass_column_entry.get()) - 1
    except ValueError:
        messagebox.showerror("Error", "Por favor, proporciona un índice de columna válido para las masas.")
        return

    # Validar archivos y directorios
    if not file_path or not output_dir or not mass_file_path:
        messagebox.showerror("Error", "Por favor, proporciona tanto un archivo de entrada como un directorio de salida y un archivo de masas.")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Leer archivo de masas como un TSV y extraer la columna especificada
    with open(mass_file_path, 'r') as mass_file:
        mass_list = []
        lines_mass = mass_file.readlines()

        # Intentar detectar encabezado
        try:
            float(lines_mass[0].strip().split()[mass_column_index])
        except ValueError:
            # Primera línea es un encabezado, omitirla
            lines_mass = lines_mass[1:]

        for line in lines_mass:
            try:
                # Extraer el valor de la columna especificada
                mass = float(line.strip().split()[mass_column_index])
                mass_list.append(mass)
            except (ValueError, IndexError):
                # Ignorar líneas que no se puedan convertir a float o que no tengan suficientes columnas
                continue

    results = []

    sequence_name = ""
    amino_sequence = ""
    PTMs = ""
    mass_mono = None
    mass_avg = None

    for line in lines:
        if line.startswith('>'):
            sequence_name = line.strip().replace('>', '')
        elif '|' in line and line.strip().startswith('mass'):
            continue
        elif '|' in line:
            try:
                mass_mono = float(line.split('|')[0].strip())
                mass_avg = float(line.split('|')[1].strip())
                mass_value = mass_mono if mass_type_input == 'mass mono' else mass_avg
                mass_value_with_correction = mass_value + mass_correction
                amino_sequence = line.split('|')[2].strip()
                PTMs = line.split('|')[3].strip()
            except ValueError:
                continue

            for target_mass in mass_list:
                lower_limit = target_mass - error
                upper_limit = target_mass + error
                if lower_limit <= mass_value_with_correction <= upper_limit:
                    results.append({
                        'Peak mass': target_mass,
                        'Peptide mass': mass_value,
                        'Mass error': abs(target_mass - mass_value),
                        'Peptide name': sequence_name,
                        'Peptide sequence': amino_sequence,
                        'Peptide PTMs': PTMs
                    })

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values(by=['Peak mass'])  # Ordenamos los valores por 'Peak mass'
        output_file_name = os.path.splitext(os.path.basename(file_path))[0] + '_filtrado_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.xlsx'
        output_file_path = os.path.join(output_dir, output_file_name)
        df.to_excel(output_file_path, index=False)
        messagebox.showinfo("Resultado", "La ejecución ha terminado con éxito")
    else:
        messagebox.showinfo("Resultado", "Ninguna secuencia ha pasado el filtro")

root = tk.Tk()
root.title("ConoMass Filter")

# Mass type
tk.Label(root, text="Tipo de Masa: ").grid(row=0, column=0)
mass_type = tk.StringVar()
mass_type.set("mass mono")  # default value
mass_type_menu = tk.OptionMenu(root, mass_type, "mass mono", "mass avg")
mass_type_menu.grid(row=0, column=1)

# Mass correction
tk.Label(root, text="Corrección de Masa: ").grid(row=1, column=0)
mass_correction_menu = tk.StringVar()
mass_correction_menu.set("0")  # default value
mass_correction_option_menu = tk.OptionMenu(root, mass_correction_menu, "-1", "0", "+1")
mass_correction_option_menu.grid(row=1, column=1)

# Error
tk.Label(root, text="Error: ").grid(row=2, column=0)
error_entry = tk.Entry(root)
error_entry.grid(row=2, column=1)

# Sequence file path
tk.Label(root, text="Archivo secuencias: ").grid(row=3, column=0)
file_entry = tk.Entry(root)
file_entry.grid(row=3, column=1)
file_button = tk.Button(root, text="Seleccionar", command=lambda: browse_file(file_entry))
file_button.grid(row=3, column=2)

# Mass file path
tk.Label(root, text="Archivo masas: ").grid(row=4, column=0)
mass_file_entry = tk.Entry(root)
mass_file_entry.grid(row=4, column=1)
mass_file_button = tk.Button(root, text="Seleccionar", command=lambda: browse_file(mass_file_entry))
mass_file_button.grid(row=4, column=2)

# Mass column index
tk.Label(root, text="¿En qué columna se encuentran las masas? (1, 2...): ").grid(row=5, column=0)
mass_column_entry = tk.Entry(root)
mass_column_entry.grid(row=5, column=1)

# Output directory
tk.Label(root, text="Directorio de salida: ").grid(row=6, column=0)
dir_entry = tk.Entry(root)
dir_entry.grid(row=6, column=1)
dir_button = tk.Button(root, text="Seleccionar", command=lambda: browse_directory(dir_entry))
dir_button.grid(row=6, column=2)

# Execute button
execute_button = tk.Button(root, text="Ejecutar", command=filter_sequences)
execute_button.grid(row=7, column=1)

root.mainloop()
