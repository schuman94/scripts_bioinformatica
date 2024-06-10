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

def extract_identifiers(fasta_file):
    identifiers = set()
    with open(fasta_file, 'r') as file:
        for line in file:
            if line.startswith('>'):
                identifier = line[1:].split()[0]
                identifiers.add(identifier)
    return identifiers

def write_identifiers_to_file(identifiers, output_file):
    with open(output_file, 'w') as file:
        for identifier in identifiers:
            file.write(identifier + '\n')

def process_directory(directory_path):
    all_identifiers = set()
    for filename in os.listdir(directory_path):
        if filename.endswith('.fasta'):
            filepath = os.path.join(directory_path, filename)
            filepath = convertir_a_ruta_larga(filepath)
            identifiers = extract_identifiers(filepath)
            all_identifiers.update(identifiers)
    return all_identifiers

def run_extraction(input_dir, output_file):
    input_dir = convertir_a_ruta_larga(input_dir)
    output_file = convertir_a_ruta_larga(output_file)
    all_identifiers = process_directory(input_dir)
    write_identifiers_to_file(all_identifiers, output_file)
    messagebox.showinfo("Información", "El proceso ha terminado.")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Input directory
        self.input_dir_label = tk.Label(self, text="Directorio de Entrada:")
        self.input_dir_label.grid(row=0, column=0, sticky="w")
        self.input_dir = tk.StringVar()
        self.input_dir_entry = tk.Entry(self, textvariable=self.input_dir, width=50)
        self.input_dir_entry.grid(row=0, column=1, sticky="w")
        self.input_dir_button = tk.Button(self, text="Seleccionar", command=self.select_input_dir)
        self.input_dir_button.grid(row=0, column=2, sticky="w")

        # Output file
        self.output_file_label = tk.Label(self, text="Archivo de Salida:")
        self.output_file_label.grid(row=1, column=0, sticky="w")
        self.output_file = tk.StringVar()
        self.output_file_entry = tk.Entry(self, textvariable=self.output_file, width=50)
        self.output_file_entry.grid(row=1, column=1, sticky="w")
        self.output_file_button = tk.Button(self, text="Seleccionar", command=self.select_output_file)
        self.output_file_button.grid(row=1, column=2, sticky="w")

        # Execute button
        self.execute_button = tk.Button(self, text="Ejecutar", command=self.execute)
        self.execute_button.grid(row=2, column=1, columnspan=2, sticky="w")

    def select_input_dir(self):
        dir_path = filedialog.askdirectory()
        self.input_dir.set(dir_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        self.output_file.set(file_path)

    def execute(self):
        input_dir = self.input_dir.get()
        output_file = self.output_file.get()
        if not input_dir or not output_file:
            messagebox.showerror("Error", "Debe seleccionar un directorio de entrada y un archivo de salida.")
            return
        run_extraction(input_dir, output_file)

def main():
    root = tk.Tk()
    root.title("Extractor de Identificadores de FASTA")
    root.geometry("700x150")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
