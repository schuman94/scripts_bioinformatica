from tkinter import filedialog
from Bio import SeqIO
import os
import datetime
import filters

def seleccionar_archivo(var):
    def inner():
        file_path = filedialog.askopenfilename(filetypes=[("Archivos FASTA", "*.fasta")])
        var.set(file_path)
    return inner

def seleccionar_carpeta(var):
    def inner():
        folder_path = filedialog.askdirectory()
        var.set(folder_path)
    return inner

def filtrar_secuencias(input_file, output_folder, filter_option, gap1=None, gap2=None, num_c=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    input_filename = os.path.splitext(os.path.basename(input_file))[0]

    if filter_option == "Patron alfa":
        filter_name = f"{filter_option}_{gap1}_{gap2}"
    elif filter_option == "C":
        filter_name = f"{filter_option}_{num_c}"
    else:
        filter_name = filter_option

    output_file = os.path.join(output_folder, f"{input_filename}_{filter_name}_{timestamp}.fasta")

    filter_func = filters.get_filter_function(filter_option, gap1, gap2, num_c)

    with open(input_file, "r") as in_handle, open(output_file, "w") as out_handle:
        records = SeqIO.parse(in_handle, "fasta")
        filtered = filter(filter_func, records)
        SeqIO.write(filtered, out_handle, "fasta")
