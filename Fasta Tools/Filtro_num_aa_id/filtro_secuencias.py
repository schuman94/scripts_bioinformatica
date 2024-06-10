import os
from tkinter import *
from tkinter import filedialog, messagebox
from Bio import SeqIO
from pathlib import Path

def convertir_a_ruta_larga(ruta):
    # Convertimos la ruta a formato extendido si estamos en Windows
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Filtrar Secuencias FASTA")
        self.pack()
        self.create_widgets()

        self.archivo_entrada = None
        self.directorio_salida = None

    def browse_archivo_entrada(self):
        self.archivo_entrada = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta"), ("All files", "*.*")])
        if self.archivo_entrada:
            self.archivo_entrada = convertir_a_ruta_larga(self.archivo_entrada)
            self.lbl_archivo_entrada.config(text=f'Archivo de Entrada: {os.path.basename(self.archivo_entrada)}')

    def browse_directorio_salida(self):
        self.directorio_salida = filedialog.askdirectory()
        if self.directorio_salida:
            self.directorio_salida = convertir_a_ruta_larga(self.directorio_salida)
            self.lbl_directorio_salida.config(text=f'Directorio de Salida: {self.directorio_salida}')

    def filtrar_secuencias(self):
        if not self.archivo_entrada or not self.directorio_salida:
            messagebox.showwarning('Advertencia', 'Selecciona el archivo de entrada y el directorio de salida antes de proceder.')
            return

        max_longitud = self.entry_max_longitud.get()
        prefijo_excluir = self.entry_prefijo_excluir.get()

        try:
            max_longitud = int(max_longitud) if max_longitud else None
        except ValueError:
            messagebox.showerror('Error', 'La longitud máxima debe ser un número entero.')
            return

        # Definir los nombres de los archivos de salida
        archivo_salida = Path(self.directorio_salida) / "fichero_resultado.fasta"
        archivo_salida = convertir_a_ruta_larga(str(archivo_salida))

        with open(archivo_salida, 'w') as salida:
            for record in SeqIO.parse(self.archivo_entrada, 'fasta'):
                if (max_longitud is None or len(record.seq) <= max_longitud) and (not prefijo_excluir or not record.description.startswith(prefijo_excluir)):
                    salida.write(f">{record.description}\n")
                    salida.write(f"{record.seq}\n")

        messagebox.showinfo('Finalizado', 'El proceso de filtrado ha finalizado con éxito.\nResultados guardados en: ' + archivo_salida)

    def create_widgets(self):
        Label(self, text="Archivo de Entrada:").pack(side="top", padx=5, pady=5)
        self.lbl_archivo_entrada = Label(self, text="Ningún archivo seleccionado")
        self.lbl_archivo_entrada.pack(side="top", padx=5, pady=5)

        Button(self, text="Seleccionar Archivo de Entrada", command=self.browse_archivo_entrada).pack(side="top", padx=5, pady=5)

        Label(self, text="Directorio de Salida:").pack(side="top", padx=5, pady=5)
        self.lbl_directorio_salida = Label(self, text="Ningún directorio seleccionado")
        self.lbl_directorio_salida.pack(side="top", padx=5, pady=5)

        Button(self, text="Seleccionar Directorio de Salida", command=self.browse_directorio_salida).pack(side="top", padx=5, pady=5)

        Label(self, text="Máxima Longitud de Secuencias (opcional):").pack(side="top", padx=5, pady=5)
        self.entry_max_longitud = Entry(self)
        self.entry_max_longitud.pack(side="top", padx=5, pady=5)
        self.entry_max_longitud.insert(0, "120")

        Label(self, text="Prefijo para Excluir Secuencias (opcional):").pack(side="top", padx=5, pady=5)
        self.entry_prefijo_excluir = Entry(self)
        self.entry_prefijo_excluir.pack(side="top", padx=5, pady=5)
        self.entry_prefijo_excluir.insert(0, "gene:")

        Button(self, text="EJECUTAR", fg="red", command=self.filtrar_secuencias).pack(side="bottom", padx=5, pady=10)

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()
