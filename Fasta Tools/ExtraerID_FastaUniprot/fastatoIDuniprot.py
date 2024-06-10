import re
import tkinter as tk
from tkinter import filedialog
import os

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def extract_identifiers(fasta_file):
    identifiers = []
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                match = re.search(r'>sp\|(.+?)\|', line)
                if match:
                    identifiers.append(match.group(1))
    return identifiers

def save_identifiers_to_txt(identifiers, output_file):
    with open(output_file, 'w') as f:
        for identifier in identifiers:
            f.write(f'{identifier}\n')

def browse_fasta_file():
    input_fasta_file = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta")])
    return input_fasta_file

def browse_output_folder():
    output_folder = filedialog.askdirectory()
    return output_folder

def main():
    root = tk.Tk()
    root.withdraw()

    input_fasta_file = browse_fasta_file()
    if not input_fasta_file:
        print("No se seleccionó ningún archivo .fasta.")
        return

    output_folder = browse_output_folder()
    if not output_folder:
        print("No se seleccionó ninguna carpeta de salida.")
        return

    # Convertir a rutas largas si es necesario
    input_fasta_file = convertir_a_ruta_larga(input_fasta_file)
    output_folder = convertir_a_ruta_larga(output_folder)

    output_txt_file = os.path.join(output_folder, "identifiers.txt")

    identifiers = extract_identifiers(input_fasta_file)
    save_identifiers_to_txt(identifiers, output_txt_file)

    print(f"Los identificadores se han guardado en {output_txt_file}")

if __name__ == '__main__':
    main()
