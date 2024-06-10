import os
import tkinter as tk
from tkinter import filedialog, messagebox
import csv

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

class TxtToCsvConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertir TXT a CSV")

        # Input directory
        tk.Label(root, text="Carpeta de Entrada:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_dir_entry = tk.Entry(root, width=50)
        self.input_dir_entry.grid(row=0, column=1, padx=5, pady=5)
        self.input_dir_button = tk.Button(root, text="Examinar", command=self.browse_input)
        self.input_dir_button.grid(row=0, column=2, padx=5, pady=5)

        # Output directory
        tk.Label(root, text="Carpeta de Salida:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_dir_entry = tk.Entry(root, width=50)
        self.output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
        self.output_dir_button = tk.Button(root, text="Examinar", command=self.browse_output)
        self.output_dir_button.grid(row=1, column=2, padx=5, pady=5)

        # Execute button
        self.execute_button = tk.Button(root, text="Ejecutar", command=self.execute)
        self.execute_button.grid(row=2, column=1, pady=5)

    def browse_input(self):
        dirname = filedialog.askdirectory()
        self.input_dir_entry.delete(0, tk.END)
        self.input_dir_entry.insert(0, dirname)

    def browse_output(self):
        dirname = filedialog.askdirectory()
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, dirname)

    def execute(self):
        input_dir = convertir_a_ruta_larga(self.input_dir_entry.get())
        output_dir = convertir_a_ruta_larga(self.output_dir_entry.get())

        if not input_dir or not output_dir:
            messagebox.showerror("Error", "Por favor, seleccione las carpetas de entrada y salida.")
            return

        try:
            for file in os.listdir(input_dir):
                if file.endswith(".txt"):
                    txt_file_path = convertir_a_ruta_larga(os.path.join(input_dir, file))
                    csv_file_path = convertir_a_ruta_larga(os.path.join(output_dir, file.replace(".txt", ".csv")))

                    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                        lines = txt_file.readlines()

                    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(["n", "file_name", "db_id", "rmsd", "tm_score", "search_mode", "search_type"])
                        for line in lines[1:]:
                            csv_writer.writerow(line.strip().split(','))

            messagebox.showinfo("Completado", "La ejecución ha finalizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = TxtToCsvConverterApp(root)
    root.mainloop()
