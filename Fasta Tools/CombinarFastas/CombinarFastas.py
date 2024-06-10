import tkinter as tk
from tkinter import filedialog, messagebox
import os

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

class FastaCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Combinar Ficheros Fasta")

        # Input directory
        tk.Label(root, text="Carpeta de Entrada:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_dir_entry = tk.Entry(root, width=50)
        self.input_dir_entry.grid(row=0, column=1, padx=5, pady=5)
        self.input_dir_button = tk.Button(root, text="Browse", command=self.browse_input)
        self.input_dir_button.grid(row=0, column=2, padx=5, pady=5)

        # Output directory
        tk.Label(root, text="Carpeta de Salida:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_dir_entry = tk.Entry(root, width=50)
        self.output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
        self.output_dir_button = tk.Button(root, text="Browse", command=self.browse_output)
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
        output_file_name = os.path.basename(os.path.normpath(input_dir)) + '.fasta'
        output_file_path = os.path.join(output_dir, output_file_name)

        try:
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                for file in os.listdir(input_dir):
                    if file.endswith(".fasta") or file.endswith(".fa"):
                        file_path = convertir_a_ruta_larga(os.path.join(input_dir, file))
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            sequence_lines = []
                            for line in infile:
                                if line.startswith('>'):
                                    if sequence_lines:
                                        # Escribe la secuencia acumulada en una sola línea
                                        outfile.write(''.join(sequence_lines) + '\n')
                                        sequence_lines = []
                                    # Escribe el encabezado inmediatamente
                                    outfile.write(line)
                                else:
                                    # Acumula las líneas de la secuencia sin el cambio de línea
                                    sequence_lines.append(line.strip())
                            # No olvides escribir la última secuencia si existe
                            if sequence_lines:
                                outfile.write(''.join(sequence_lines) + '\n')

            messagebox.showinfo("Completado", "La ejecución ha finalizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FastaCombinerApp(root)
    root.mainloop()
