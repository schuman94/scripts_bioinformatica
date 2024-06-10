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
        self.pack()
        self.create_widgets()

        self.fichero1 = None
        self.fichero2 = None
        self.output_directory = None

    def browse_fichero1(self):
        self.fichero1 = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta"), ("All files", "*.*")])
        if self.fichero1:
            self.lbl_fichero1.config(text=f'Fichero 1: {os.path.basename(self.fichero1)}')

    def browse_fichero2(self):
        self.fichero2 = filedialog.askopenfilename(filetypes=[("FASTA files", "*.fasta"), ("All files", "*.*")])
        if self.fichero2:
            self.lbl_fichero2.config(text=f'Fichero 2: {os.path.basename(self.fichero2)}')

    def browse_output_directory(self):
        self.output_directory = filedialog.askdirectory()
        if self.output_directory:
            self.lbl_output_directory.config(text=f'Directorio de Salida: {self.output_directory}')

    def process_files(self):
        if not self.fichero1 or not self.fichero2 or not self.output_directory:
            messagebox.showwarning('Advertencia', 'Selecciona ambos ficheros y el directorio de salida antes de proceder.')
            return

        fichero_resultado = Path(self.output_directory) / "fichero_resultado.fasta"
        secuencias_no_encontradas = Path(self.output_directory) / "secuencias_no_encontradas.fasta"

        # Leer las secuencias del fichero2 y almacenarlas en un conjunto
        secuencias_fichero2 = set(str(record.seq) for record in SeqIO.parse(convertir_a_ruta_larga(self.fichero2), 'fasta'))
        secuencias_eliminar = set()

        # Abrir el fichero de resultado en modo de escritura
        with open(fichero_resultado, 'w') as resultado:
            # Iterar sobre cada registro en fichero1
            for record in SeqIO.parse(convertir_a_ruta_larga(self.fichero1), 'fasta'):
                # Si la secuencia está en el conjunto de secuencias del fichero2
                if str(record.seq) in secuencias_fichero2:
                    secuencias_eliminar.add(str(record.seq))
                else:
                    # Escribir la descripción y la secuencia en el fichero de resultado
                    resultado.write(f">{record.description}\n")
                    resultado.write(f"{record.seq}\n")

        # Escribir las secuencias del fichero2 que no se encontraron en el fichero1
        with open(secuencias_no_encontradas, 'w') as no_encontradas:
            for record in SeqIO.parse(convertir_a_ruta_larga(self.fichero2), 'fasta'):
                if str(record.seq) not in secuencias_eliminar:
                    no_encontradas.write(f">{record.description}\n")
                    no_encontradas.write(f"{record.seq}\n")

        messagebox.showinfo('Finalizado', f'Proceso completado.\nResultados guardados en: {fichero_resultado}\nSecuencias no encontradas en: {secuencias_no_encontradas}')

    def create_widgets(self):
        self.btn_fichero1 = Button(self)
        self.btn_fichero1["text"] = "Seleccionar Fichero 1"
        self.btn_fichero1["command"] = self.browse_fichero1
        self.btn_fichero1.pack(side="top")

        self.lbl_fichero1 = Label(self, text="")
        self.lbl_fichero1.pack(side="top")

        self.btn_fichero2 = Button(self)
        self.btn_fichero2["text"] = "Seleccionar Fichero 2"
        self.btn_fichero2["command"] = self.browse_fichero2
        self.btn_fichero2.pack(side="top")

        self.lbl_fichero2 = Label(self, text="")
        self.lbl_fichero2.pack(side="top")

        self.btn_output_directory = Button(self)
        self.btn_output_directory["text"] = "Seleccionar Directorio de Salida"
        self.btn_output_directory["command"] = self.browse_output_directory
        self.btn_output_directory.pack(side="top")

        self.lbl_output_directory = Label(self, text="")
        self.lbl_output_directory.pack(side="top")

        self.btn_execute = Button(self, text="EJECUTAR", fg="red", command=self.process_files)
        self.btn_execute.pack(side="bottom")

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.master.title('Filtrar FASTA por Diferencia de Conjuntos')
    app.mainloop()
