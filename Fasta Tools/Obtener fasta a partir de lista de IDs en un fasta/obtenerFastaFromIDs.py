import os
from tkinter import filedialog, messagebox, StringVar, Entry, Button, Label, Tk
from Bio import SeqIO

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def select_id_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    id_file.set(filename)

def select_fasta_file():
    filename = filedialog.askopenfilename(filetypes=[("Fasta files", "*.fasta")])
    fasta_file.set(filename)

def select_output_directory():
    dirname = filedialog.askdirectory()
    output_directory.set(dirname)

def execute():
    id_file_path = convertir_a_ruta_larga(id_file.get())
    fasta_file_path = convertir_a_ruta_larga(fasta_file.get())
    output_dir = convertir_a_ruta_larga(output_directory.get())

    try:
        # Leer los IDs del archivo txt
        with open(id_file_path, 'r') as id_handle:
            id_list = [line.strip() for line in id_handle]

        # Crear el archivo fasta de resultados
        resultados_path = os.path.join(output_dir, 'resultados.fasta')
        with open(resultados_path, 'w') as resultados_handle:
            # Leer el archivo fasta y buscar los IDs
            for record in SeqIO.parse(fasta_file_path, "fasta"):
                if record.id in id_list:
                    resultados_handle.write(f">{record.id}\n{str(record.seq)}\n")

        messagebox.showinfo("Finalizado", "Proceso completado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

root = Tk()
root.title("Filtrar Secuencias Fasta")

id_file = StringVar()
fasta_file = StringVar()
output_directory = StringVar()

Label(root, text="ID file").grid(row=0, column=0)
Entry(root, textvariable=id_file).grid(row=0, column=1)
Button(root, text="Examinar", command=select_id_file).grid(row=0, column=2)

Label(root, text="Fasta file").grid(row=1, column=0)
Entry(root, textvariable=fasta_file).grid(row=1, column=1)
Button(root, text="Examinar", command=select_fasta_file).grid(row=1, column=2)

Label(root, text="Output directory").grid(row=2, column=0)
Entry(root, textvariable=output_directory).grid(row=2, column=1)
Button(root, text="Examinar", command=select_output_directory).grid(row=2, column=2)

Button(root, text="Ejecutar", command=execute).grid(row=3, column=0, columnspan=3)

root.mainloop()
