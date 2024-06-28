import os
import pandas as pd
from Bio import SeqIO
import tkinter as tk
from tkinter import filedialog, messagebox

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def browse_fasta_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_output_file(entry):
    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx;*.xls")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def execute_conversion(fasta_file_entry, output_file_entry):
    fasta_file = convertir_a_ruta_larga(fasta_file_entry.get())
    output_file = convertir_a_ruta_larga(output_file_entry.get())

    if not fasta_file or not output_file:
        messagebox.showerror("Error", "Por favor, seleccione un archivo FASTA y un archivo de salida.")
        return

    try:
        records = []
        for record in SeqIO.parse(fasta_file, "fasta"):
            identifier = record.id
            sequence = str(record.seq)
            records.append((identifier, sequence))

        df = pd.DataFrame(records, columns=["ID", "Sequence"])
        df.to_excel(output_file, index=False)

        messagebox.showinfo("Éxito", f"Archivo Excel generado exitosamente en {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def main():
    root = tk.Tk()
    root.title("FASTA to Excel Converter")

    # Etiquetas y entradas
    tk.Label(root, text="Archivo FASTA").grid(row=0, column=0, sticky=tk.W)
    fasta_file_entry = tk.Entry(root, width=50)
    fasta_file_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_fasta_file(fasta_file_entry)).grid(row=0, column=2)

    tk.Label(root, text="Archivo de salida (Excel)").grid(row=1, column=0, sticky=tk.W)
    output_file_entry = tk.Entry(root, width=50)
    output_file_entry.grid(row=1, column=1)
    tk.Button(root, text="Guardar como", command=lambda: browse_output_file(output_file_entry)).grid(row=1, column=2)

    # Botón de ejecución
    tk.Button(root, text="Convertir", command=lambda: execute_conversion(fasta_file_entry, output_file_entry)).grid(row=2, column=0, columnspan=3)

    # Mantener la ventana abierta
    root.mainloop()

if __name__ == '__main__':
    main()
