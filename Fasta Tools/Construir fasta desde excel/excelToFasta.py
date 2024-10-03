import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def clean_text(text):
    # Eliminar caracteres problemáticos, como el espacio de ancho cero
    return str(text).replace('\u200b', '')

def browse_excel_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_output_file(entry):
    filename = filedialog.asksaveasfilename(defaultextension=".fasta", filetypes=[("FASTA files", "*.fasta")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def execute_conversion(excel_file_entry, output_file_entry):
    excel_file = convertir_a_ruta_larga(excel_file_entry.get())
    output_file = convertir_a_ruta_larga(output_file_entry.get())

    if not excel_file or not output_file:
        messagebox.showerror("Error", "Por favor, seleccione un archivo Excel y un archivo de salida.")
        return

    try:
        df = pd.read_excel(excel_file)
        if df.shape[1] < 2:
            messagebox.showerror("Error", "El archivo Excel debe tener al menos dos columnas.")
            return

        with open(output_file, 'w', encoding='utf-8') as fasta_file:
            for index, row in df.iterrows():
                identifier = clean_text(row.iloc[0])
                sequence = clean_text(row.iloc[1])
                fasta_file.write(f'>{identifier}\n')
                fasta_file.write(f'{sequence}\n')

        messagebox.showinfo("Éxito", f"Archivo FASTA generado exitosamente en {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Excel to FASTA Converter")

    # Etiquetas y entradas
    tk.Label(root, text="Archivo Excel").grid(row=0, column=0, sticky=tk.W)
    excel_file_entry = tk.Entry(root, width=50)
    excel_file_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_excel_file(excel_file_entry)).grid(row=0, column=2)

    tk.Label(root, text="Archivo de salida (FASTA)").grid(row=1, column=0, sticky=tk.W)
    output_file_entry = tk.Entry(root, width=50)
    output_file_entry.grid(row=1, column=1)
    tk.Button(root, text="Guardar como", command=lambda: browse_output_file(output_file_entry)).grid(row=1, column=2)

    # Botón de ejecución
    tk.Button(root, text="Convertir", command=lambda: execute_conversion(excel_file_entry, output_file_entry)).grid(row=2, column=0, columnspan=3)

    # Mantener la ventana abierta
    root.mainloop()

if __name__ == '__main__':
    main()
