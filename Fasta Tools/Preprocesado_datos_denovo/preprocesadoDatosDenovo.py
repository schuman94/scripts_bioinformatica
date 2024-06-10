import pandas as pd
import re
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def parse_csv_to_fasta(csv_file, quality_threshold, output_file):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)

    # Convertir la columna ALC(%) a tipo numérico
    df['ALC (%)'] = pd.to_numeric(df['ALC (%)'], errors='coerce')

    # Filtrar las filas basado en el porcentaje de calidad (ALC)
    df_filtered = df[df['ALC (%)'] >= quality_threshold]

    # Función para eliminar información entre paréntesis
    def remove_parenthesis_info(sequence):
        return re.sub(r'\(.*?\)', '', sequence)

    # Eliminar información entre paréntesis en la columna 'Peptide'
    df_filtered['Peptide'] = df_filtered['Peptide'].apply(remove_parenthesis_info)

    # Crear el archivo FASTA
    with open(output_file, 'w') as fasta_file:
        for _, row in df_filtered.iterrows():
            fasta_file.write(f'>{row["Source File"]}_{row["Scan"]}\n')
            fasta_file.write(f'{row["Peptide"]}\n')

def browse_csv_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_output_file(entry):
    filename = filedialog.asksaveasfilename(defaultextension=".fasta", filetypes=[("FASTA files", "*.fasta")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def execute_conversion():
    input_csv = convertir_a_ruta_larga(csv_file_entry.get())
    quality = float(quality_entry.get())
    output_fasta = convertir_a_ruta_larga(output_file_entry.get())

    if not input_csv or not output_fasta:
        messagebox.showerror("Error", "Por favor, selecciona un archivo CSV y un archivo de salida.")
        return

    try:
        parse_csv_to_fasta(input_csv, quality, output_fasta)
        messagebox.showinfo("Éxito", f"Archivo FASTA generado exitosamente en {output_fasta}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear ventana principal
root = tk.Tk()
root.title("CSV to FASTA Converter")

# Etiquetas y entradas
tk.Label(root, text="Archivo CSV").grid(row=0, column=0, sticky=tk.W)
csv_file_entry = tk.Entry(root, width=50)
csv_file_entry.grid(row=0, column=1)
tk.Button(root, text="Abrir", command=lambda: browse_csv_file(csv_file_entry)).grid(row=0, column=2)

tk.Label(root, text="Porcentaje de calidad (ALC %)").grid(row=1, column=0, sticky=tk.W)
quality_entry = tk.Entry(root, width=50)
quality_entry.grid(row=1, column=1)

tk.Label(root, text="Archivo de salida (FASTA)").grid(row=2, column=0, sticky=tk.W)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=2, column=1)
tk.Button(root, text="Guardar como", command=lambda: browse_output_file(output_file_entry)).grid(row=2, column=2)

# Botón de ejecución
tk.Button(root, text="Convertir", command=execute_conversion).grid(row=3, column=0, columnspan=3)

# Mantener la ventana abierta
root.mainloop()
