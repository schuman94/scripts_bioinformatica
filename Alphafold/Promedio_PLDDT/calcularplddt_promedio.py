import os
import json
import pandas as pd
import numpy as np
from tkinter import filedialog, messagebox, Tk, Button, Entry, Label, StringVar, Frame

def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

class App:
    def __init__(self, root):
        self.root = root
        root.title("Registrar valores PLDDT")

        # Carpeta de entrada
        self.input_frame = Frame(root)
        self.input_frame.pack(padx=10, pady=5, fill="x")

        self.input_folder_label = Label(self.input_frame, text="Carpeta de entrada", width=20, anchor="w")
        self.input_folder_label.pack(side="left")

        self.input_folder_var = StringVar()
        self.input_folder_entry = Entry(self.input_frame, textvariable=self.input_folder_var, bd=2, width=40)
        self.input_folder_entry.pack(side="left", fill="x", expand=True)

        self.browse_input_button = Button(self.input_frame, text="Buscar", command=self.browse_input)
        self.browse_input_button.pack(side="left")

        # Carpeta de salida
        self.output_frame = Frame(root)
        self.output_frame.pack(padx=10, pady=5, fill="x")

        self.output_folder_label = Label(self.output_frame, text="Carpeta de salida", width=20, anchor="w")
        self.output_folder_label.pack(side="left")

        self.output_folder_var = StringVar()
        self.output_folder_entry = Entry(self.output_frame, textvariable=self.output_folder_var, bd=2, width=40)
        self.output_folder_entry.pack(side="left", fill="x", expand=True)

        self.browse_output_button = Button(self.output_frame, text="Buscar", command=self.browse_output)
        self.browse_output_button.pack(side="left")

        # Botón Ejecutar
        self.execute_button = Button(root, text="Ejecutar", command=self.execute, width=15, height=2, bd=2)
        self.execute_button.pack(padx=10, pady=10)

    def browse_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder_var.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder_var.set(folder)

    def execute(self):
        input_folder = convertir_a_ruta_larga(self.input_folder_var.get())
        output_folder = convertir_a_ruta_larga(self.output_folder_var.get())

        if not input_folder or not output_folder:
            messagebox.showwarning("Advertencia", "Selecciona ambas carpetas antes de ejecutar.")
            return

        records = []

        for subdir, _, _ in os.walk(input_folder):
            if subdir.endswith("env"):
                for file in os.listdir(subdir):
                    if file.endswith(".json") and "_scores_rank_001_alphafold2_ptm_model" in file:
                        with open(convertir_a_ruta_larga(os.path.join(subdir, file)), "r") as json_file:
                            data = json.load(json_file)
                            plddt = np.mean(data['plddt'])
                            protein_name = file.split("_scores_rank")[0]
                            records.append((protein_name, plddt))

        df = pd.DataFrame(records, columns=["Proteina", "Media PLDDT"])
        df.to_excel(convertir_a_ruta_larga(os.path.join(output_folder, "registro_plddt.xlsx")), index=False)

        messagebox.showinfo("Información", f"Registro completado. Revise el archivo 'registro_plddt.xlsx' en {output_folder} para más detalles.")

root = Tk()
app = App(root)
root.mainloop()
