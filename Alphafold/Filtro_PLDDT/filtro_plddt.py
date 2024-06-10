import os
import json
import shutil
import pandas as pd
import numpy as np
from tkinter import filedialog, messagebox, Tk, Button, Entry, Label, StringVar, DoubleVar, Frame

def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

class App:
    def __init__(self, root):
        self.root = root
        root.title("Filtrar y mover archivos PDB")

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

        # Valor del filtro
        self.filter_frame = Frame(root)
        self.filter_frame.pack(padx=10, pady=5, fill="x")

        self.filter_value_label = Label(self.filter_frame, text="Valor del filtro", width=20, anchor="w")
        self.filter_value_label.pack(side="left")

        self.filter_value_var = DoubleVar(value=69.5)  # Valor predeterminado
        self.filter_value_entry = Entry(self.filter_frame, textvariable=self.filter_value_var, bd=2, width=40)
        self.filter_value_entry.pack(side="left", fill="x", expand=True)

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

        log_folder = convertir_a_ruta_larga(os.path.join(output_folder, 'log'))
        os.makedirs(log_folder, exist_ok=True)

        records = []
        errors = []
        passed_count = 0  # Contador para las proteínas que pasan el filtro

        for subdir, _, _ in os.walk(input_folder):
            if subdir.endswith("env"):
                found_json = False
                for file in os.listdir(subdir):
                    if file.endswith(".json") and "_scores_rank_001_alphafold2_ptm_model" in file:
                        found_json = True
                        with open(convertir_a_ruta_larga(os.path.join(subdir, file)), "r") as json_file:
                            data = json.load(json_file)
                            plddt = np.mean(data['plddt'])
                            protein_name = file.split("_scores_rank")[0]
                            passed = plddt >= self.filter_value_var.get()
                            records.append((protein_name, plddt, passed))

                            if passed:
                                passed_count += 1  # Aumentar el contador si pasa el filtro
                                pdb_file = file.replace("_scores_", "_unrelaxed_").replace(".json", ".pdb")
                                pdb_path = convertir_a_ruta_larga(os.path.join(subdir, pdb_file))

                                if os.path.exists(pdb_path):
                                    print(f"Copiando {pdb_path} a {output_folder}")
                                    shutil.copy(pdb_path, output_folder)
                                else:
                                    print(f"Archivo no encontrado: {pdb_path}")

                if not found_json:
                    errors.append((os.path.basename(subdir),))

        df = pd.DataFrame(records, columns=["Proteina", "Media PLDDT", "Pasa Filtro"])
        df.to_csv(os.path.join(log_folder, "log.csv"), index=False)

        if errors:
            error_df = pd.DataFrame(errors, columns=["Subcarpeta Sin JSON"])
            error_df.to_csv(os.path.join(log_folder, "error.csv"), index=False)

        messagebox.showinfo("Información", f"Ejecución completada. {passed_count} proteínas han pasado el filtro. Revise la consola para más detalles.")

root = Tk()
app = App(root)
root.mainloop()
