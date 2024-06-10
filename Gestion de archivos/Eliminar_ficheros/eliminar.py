import os
from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import Path

def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.txt_file = None
        self.directory = None
        self.pack()
        self.create_widgets()

    def select_txt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.txt_file = file_path
            self.lbl_txt.config(text=f'TXT seleccionado: {os.path.basename(file_path)}')

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory = directory
            self.lbl_dir.config(text=f'Directorio seleccionado: {directory}')

    def delete_files(self):
        if not self.txt_file or not self.directory:
            messagebox.showwarning('Advertencia', 'Selecciona el archivo TXT y el directorio antes de proceder.')
            return

        count = 0
        with open(convertir_a_ruta_larga(self.txt_file), 'r') as file:
            nombres = [line.strip() for line in file.readlines()]

        for nombre in nombres:
            for item in Path(convertir_a_ruta_larga(self.directory)).glob('*'):
                if nombre in item.name:
                    try:
                        item_path = convertir_a_ruta_larga(str(item))
                        Path(item_path).unlink()
                        count += 1
                    except Exception as e:
                        print(f'No se pudo eliminar el archivo {item.name}. Error: {e}')

        messagebox.showinfo('Finalizado', f'Se ha terminado y se han eliminado un total de {count} archivos.')

    def create_widgets(self):
        self.btn_txt = Button(self)
        self.btn_txt["text"] = "Seleccionar TXT"
        self.btn_txt["command"] = self.select_txt_file
        self.btn_txt.pack(side="top")

        self.lbl_txt = Label(self, text="")
        self.lbl_txt.pack(side="top")

        self.btn_dir = Button(self)
        self.btn_dir["text"] = "Seleccionar Directorio"
        self.btn_dir["command"] = self.select_directory
        self.btn_dir.pack(side="top")

        self.lbl_dir = Label(self, text="")
        self.lbl_dir.pack(side="top")

        self.btn_execute = Button(self, text="EJECUTAR", fg="red", command=self.delete_files)
        self.btn_execute.pack(side="bottom")

root = Tk()
app = Application(master=root)
app.mainloop()
