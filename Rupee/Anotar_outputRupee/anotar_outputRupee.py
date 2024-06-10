import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import re

def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def browse_csv_directory():
    directory = filedialog.askdirectory()
    csv_directory_var.set(directory)

def browse_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")])
    excel_file_var.set(file_path)

def process_files():
    csv_directory = convertir_a_ruta_larga(csv_directory_var.get())
    excel_file_path = convertir_a_ruta_larga(excel_file_var.get())

    if not csv_directory or not excel_file_path:
        messagebox.showerror("Error", "Please select both the CSV directory and the Excel file.")
        return

    # Leer el archivo Excel
    excel_df = pd.read_excel(excel_file_path)

    # Crear el DataFrame de salida
    output_df = pd.DataFrame(columns=[
        "file_name", "db_id", "rmsd/tm_score",
        "pharmacological_family", "description", "function"
    ])

    # Procesar cada archivo CSV en el directorio
    for csv_file in os.listdir(csv_directory):
        if csv_file.endswith(".csv"):
            csv_file_path = convertir_a_ruta_larga(os.path.join(csv_directory, csv_file))
            df = pd.read_csv(csv_file_path)

            # Crear la nueva columna rmsd/tm_score
            df["rmsd/tm_score"] = df["rmsd"] / df["tm_score"]

            # Obtener la fila con el valor rmsd/tm_score más cercano a 0
            df = df[df["rmsd/tm_score"] > 0]  # Asegurarse de que el valor sea positivo
            selected_row = df.loc[df["rmsd/tm_score"].idxmin()]

            file_name = selected_row["file_name"]
            db_id = selected_row["db_id"]
            rmsd_tm_score = selected_row["rmsd/tm_score"]

            # Procesar file_name
            file_name_match = re.match(r"^(.*?)_unrelaxed_rank", file_name)
            if file_name_match:
                file_name = file_name_match.group(1)

            # Procesar db_id
            if db_id.startswith("AF-"):
                db_id = re.match(r"AF-(.*?)-F1-model", db_id).group(1)
            else:
                db_id = re.match(r"^(.*?)_unrelaxed", db_id).group(1)

            # Buscar en el Excel el db_id correspondiente
            excel_row = excel_df[excel_df.iloc[:, 0] == db_id]
            if not excel_row.empty:
                pharmacological_family = excel_row.iloc[0, 8]  # Novena columna
                description = excel_row.iloc[0, 10]            # Undécima columna
                function = excel_row.iloc[0, 11]               # Duodécima columna
                if function.startswith("FUNCTION: "):
                    function = function[len("FUNCTION: "):]

                # Añadir los valores al DataFrame de salida
                new_row = pd.DataFrame({
                    "file_name": [file_name],
                    "db_id": [db_id],
                    "rmsd/tm_score": [rmsd_tm_score],
                    "pharmacological_family": [pharmacological_family],
                    "description": [description],
                    "function": [function]
                })

                output_df = pd.concat([output_df, new_row], ignore_index=True)

    # Guardar el DataFrame de salida en un archivo Excel
    output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx *.xls *.xlsm")])
    if output_file_path:
        output_df.to_excel(output_file_path, index=False)
        messagebox.showinfo("Success", "The files have been processed and saved successfully.")

app = tk.Tk()
app.title("Rupee CSV Processor")

for i in range(3):
    app.columnconfigure(i, weight=1, minsize=100)
    app.rowconfigure(i, weight=1, minsize=50)

csv_directory_label = tk.Label(app, text="CSV Directory:")
csv_directory_label.grid(column=0, row=0, sticky="e", padx=5, pady=5)

csv_directory_var = tk.StringVar()
csv_directory_entry = tk.Entry(app, textvariable=csv_directory_var, width=50)
csv_directory_entry.grid(column=1, row=0, sticky="ew", padx=5, pady=5)

browse_csv_button = tk.Button(app, text="Browse", command=browse_csv_directory)
browse_csv_button.grid(column=2, row=0, sticky="w", padx=5, pady=5)

excel_file_label = tk.Label(app, text="Excel File:")
excel_file_label.grid(column=0, row=1, sticky="e", padx=5, pady=5)

excel_file_var = tk.StringVar()
excel_file_entry = tk.Entry(app, textvariable=excel_file_var, width=50)
excel_file_entry.grid(column=1, row=1, sticky="ew", padx=5, pady=5)

browse_excel_button = tk.Button(app, text="Browse", command=browse_excel_file)
browse_excel_button.grid(column=2, row=1, sticky="w", padx=5, pady=5)

process_button = tk.Button(app, text="Process", command=process_files)
process_button.grid(column=1, row=2, sticky="ew", padx=5, pady=5)

app.mainloop()
