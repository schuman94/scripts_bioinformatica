#!/usr/bin/env python3
import argparse
from Bio import SeqIO
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def fasta_split(infile, outdir, num):
    record_iter = SeqIO.parse(open(infile),"fasta")
    count = 0
    file_num = 1
    records = []
    base = os.path.basename(infile)
    base_name = os.path.splitext(base)[0]

    for record in record_iter:
        record.seq = record.seq.upper() # convert sequence to uppercase
        records.append(record)
        if (count + 1) % num == 0:
            output_path = os.path.join(outdir, "{}_{}.fasta".format(base_name, file_num))
            output_path = convertir_a_ruta_larga(output_path)
            with open(output_path, "w") as output_handle:
                SeqIO.write(records, output_handle, "fasta")
            file_num += 1
            records = []
        count += 1
    if records:
        output_path = os.path.join(outdir, "{}_{}.fasta".format(base_name, file_num))
        output_path = convertir_a_ruta_larga(output_path)
        with open(output_path, "w") as output_handle:
            SeqIO.write(records, output_handle, "fasta")
    return f"Total sequences processed: {count}"

def fasta_merge(indir, outfile):
    records = []
    for file_name in os.listdir(indir):
        if file_name.endswith(".fasta"):
            file_path = os.path.join(indir, file_name)
            file_path = convertir_a_ruta_larga(file_path)
            record_iter = SeqIO.parse(open(file_path),"fasta")
            for record in record_iter:
                record.seq = record.seq.upper() # convert sequence to uppercase
                records.append(record)

    with open(outfile, "w") as output_handle:
        SeqIO.write(records, output_handle, "fasta")
    return f"Total sequences in merged file: {len(records)}"

def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, 'end')
    entry.insert(0, filename)

def browse_dir(entry):
    dirname = filedialog.askdirectory()
    entry.delete(0, 'end')
    entry.insert(0, dirname)

def main():
    root = tk.Tk()
    root.title("Split FASTA files")
    root.geometry("470x180")  # width x height in pixels

    # File
    file_label = tk.Label(root, text="File:")
    file_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
    file_entry = tk.Entry(root, width=50)
    file_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))
    file_button = tk.Button(root, text="Browse", command=lambda: browse_file(file_entry))
    file_button.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))

    # Directory
    dir_label = tk.Label(root, text="Directory:")
    dir_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
    dir_entry = tk.Entry(root, width=50)
    dir_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 0))
    dir_button = tk.Button(root, text="Browse", command=lambda: browse_dir(dir_entry))
    dir_button.grid(row=1, column=2, padx=(10, 0), pady=(10, 0))

    # Mode
    mode_label = tk.Label(root, text="Mode:")
    mode_label.grid(row=2, column=0, padx=(10, 0), pady=(10, 0))
    mode_combo = ttk.Combobox(root, values=["split"]) # Modo "merge" desactivado. Para activarlo hay que añadirlo a los values.
    mode_combo.set("split")  # Set default value
    mode_combo.grid(row=2, column=1, padx=(0, 10), pady=(10, 0), sticky='w')

    # Number
    num_label = tk.Label(root, text="Number:")
    num_label.grid(row=3, column=0, padx=(10, 0), pady=(10, 0))
    num_entry = tk.Entry(root, width=10)
    num_entry.grid(row=3, column=1, padx=(0, 10), pady=(10, 0), sticky='w')

    def execute():
        file_path = convertir_a_ruta_larga(file_entry.get())
        dir_path = convertir_a_ruta_larga(dir_entry.get())
        mode = mode_combo.get()
        num = num_entry.get()

        if not file_path or not dir_path or not mode:
            messagebox.showinfo("Error", "Please fill out all fields")
        else:
            if mode == "split":
                if not num:
                    messagebox.showinfo("Error", "Please fill out the number field for 'split' mode")
                else:
                    try:
                        message = fasta_split(file_path, dir_path, int(num))
                        messagebox.showinfo("Result", message)
                    except ValueError:
                        messagebox.showinfo("Error", "Number must be an integer")
            else:
                message = fasta_merge(dir_path, file_path)
                messagebox.showinfo("Result", message)

    exec_button = tk.Button(root, text="Execute", command=execute)
    exec_button.grid(row=4, column=0, columnspan=3, padx=(10, 0), pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    main()
