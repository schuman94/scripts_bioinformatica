import os
import re
from tkinter import filedialog, messagebox, StringVar, Entry, Button, Label, Tk
from Bio import SeqIO

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def select_input_file():
    filename = filedialog.askopenfilename(filetypes=[("Fasta files", "*.fasta")])
    input_file.set(filename)

def select_output_directory():
    dirname = filedialog.askdirectory()
    output_directory.set(dirname)

def execute():
    fasta_file = convertir_a_ruta_larga(input_file.get())
    output_dir = convertir_a_ruta_larga(output_directory.get())

    try:
        fasta_basename = os.path.basename(fasta_file)
        fasta_name = os.path.splitext(fasta_basename)[0]
        output_dir = os.path.join(output_dir, fasta_name)
        os.makedirs(output_dir, exist_ok=True)

        with open(fasta_file, "r") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                record_name = re.sub(r'\W+', '_', record.name)
                output_file = os.path.join(output_dir, f"{record_name}.fasta")
                output_file = convertir_a_ruta_larga(output_file)
                with open(output_file, "w") as output_handle:
                    output_handle.write(f">{record_name}\n")
                    output_handle.write(str(record.seq))

        messagebox.showinfo("Finalizado", "Proceso completado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

root = Tk()
root.title("Separar Fasta")
input_file = StringVar()
output_directory = StringVar()

Label(root, text="Fasta file").grid(row=0, column=0)
Entry(root, textvariable=input_file).grid(row=0, column=1)
Button(root, text="Examinar", command=select_input_file).grid(row=0, column=2)

Label(root, text="Output directory").grid(row=1, column=0)
Entry(root, textvariable=output_directory).grid(row=1, column=1)
Button(root, text="Examinar", command=select_output_directory).grid(row=1, column=2)

Button(root, text="Ejecutar", command=execute).grid(row=2, column=0, columnspan=3)

root.mainloop()
