import os
import pandas as pd
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox

# Función para convertir rutas a formato largo en Windows
def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def process_file(file_path):
    # Leer el contenido del archivo, asegurándonos de que funcione con .csv y .txt
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        lines = file.readlines()[1:]  # Ignorar la primera línea que contiene los nombres de las columnas

    min_coefficient = float('inf')
    min_line = None
    first_data_line = None

    for i, line in enumerate(lines):
        columns = line.strip().split(',')  # Dividir las columnas por coma
        coefficient = float(columns[3]) / float(columns[4])
        if i == 0:
            first_data_line = [columns[1], columns[2], coefficient]
        if coefficient < min_coefficient:
            min_coefficient = coefficient
            min_line = [columns[1], columns[2], coefficient]

    # Si la primera línea de datos no es la misma que la línea con el coeficiente más pequeño, incluir ambas
    return [first_data_line, min_line] if first_data_line != min_line else [min_line]

def create_xlsx(input_folder, output_folder):
    # Convertir rutas a formato largo si es necesario
    input_folder = convertir_a_ruta_larga(input_folder)
    output_folder = convertir_a_ruta_larga(output_folder)

    output_file_path = os.path.join(output_folder, 'output.xlsx')

    # Crear una lista para almacenar todos los datos
    all_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt') or file_name.endswith('.csv'):  # Aceptar tanto TXT como CSV
            file_path = os.path.join(input_folder, file_name)
            file_path = convertir_a_ruta_larga(file_path)  # Convertir a ruta larga
            lines_to_write = process_file(file_path)
            all_data.extend(lines_to_write)

    # Crear un DataFrame y escribirlo en un archivo Excel
    df = pd.DataFrame(all_data, columns=['Query', 'Match', 'rmsd/tmscore'])
    df.to_excel(output_file_path, index=False)

    messagebox.showinfo("Completado", "La ejecución ha finalizado y el archivo Excel ha sido creado.")

# Funciones para la interfaz gráfica
def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, 'end')
    entry.insert(0, folder_selected)

def run_script():
    input_folder = entry_input.get()
    output_folder = entry_output.get()
    create_xlsx(input_folder, output_folder)

app = Tk()
app.title('Rupee to XLSX')

label_input = Label(app, text='Directorio de entrada:')
label_input.grid(column=0, row=0)
entry_input = Entry(app, width=50)
entry_input.grid(column=1, row=0)
button_input = Button(app, text="Browse", command=lambda: browse_folder(entry_input))
button_input.grid(column=2, row=0)

label_output = Label(app, text='Directorio de salida:')
label_output.grid(column=0, row=1)
entry_output = Entry(app, width=50)
entry_output.grid(column=1, row=1)
button_output = Button(app, text="Browse", command=lambda: browse_folder(entry_output))
button_output.grid(column=2, row=1)

button_run = Button(app, text="Ejecutar", command=run_script)
button_run.grid(column=1, row=2)

app.mainloop()
