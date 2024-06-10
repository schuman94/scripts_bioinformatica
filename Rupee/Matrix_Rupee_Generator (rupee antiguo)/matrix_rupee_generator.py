from tkinter import filedialog, messagebox, Tk, Label, Button, Entry, StringVar, OptionMenu
import os
from datetime import datetime
import pandas as pd

def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def browse_button(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, "end")
    entry.insert(0, directory)

def analisis_cluster(input_dir, output_dir, mode):
    input_dir = convertir_a_ruta_larga(input_dir)
    output_dir = convertir_a_ruta_larga(output_dir)

    archivos = os.listdir(input_dir)
    proteinas = [archivo.replace(".txt", "").split('-filtered')[0] for archivo in archivos]

    if mode == 'rmsd':
        default_value = ''
    elif mode == 'tm_score':
        default_value = 0
    else:  # mode == 'ratio'
        default_value = ''

    data = {proteina: [default_value] * len(proteinas) for proteina in proteinas}

    for archivo in archivos:
        df = pd.read_csv(os.path.join(input_dir, archivo))
        df['db_id'] = df['db_id'].apply(lambda x: x.split('-filtered')[0])

        if mode == 'ratio':
            df['ratio'] = df['rmsd'] / df['tm_score']

        for i, row in df.iterrows():
            if row['db_id'] in proteinas:
                data[archivo.replace(".txt", "").split('-filtered')[0]][proteinas.index(row['db_id'])] = row[mode]

    df = pd.DataFrame(data, columns=proteinas, index=proteinas)
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(os.path.join(output_dir, f"Matrix_{mode}_{fecha_actual}.csv"), sep=",")
    df.to_excel(os.path.join(output_dir, f"Matrix_{mode}_{fecha_actual}.xlsx"))
    messagebox.showinfo("Execution Complete", f"{mode.capitalize()} Matrix created successfully")

def execute(entry_in, entry_out, mode_var):
    input_dir = convertir_a_ruta_larga(entry_in.get())
    output_dir = convertir_a_ruta_larga(entry_out.get())
    mode = mode_var.get()

    if not input_dir or not output_dir:
        messagebox.showerror("Error", "Please fill in all fields before executing")
    else:
        analisis_cluster(input_dir, output_dir, mode)

def main():
    window = Tk()
    window.title("Matrix Rupee Generator")
    window.geometry('525x120')

    Label(window, text="Input Directory:").grid(row=0, sticky='W')
    entry_in = Entry(window, width=60)
    entry_in.grid(row=0, column=1)
    Button(window, text="Browse", command=lambda: browse_button(entry_in)).grid(row=0, column=2)

    Label(window, text="Output Directory:").grid(row=1, sticky='W')
    entry_out = Entry(window, width=60)
    entry_out.grid(row=1, column=1)
    Button(window, text="Browse", command=lambda: browse_button(entry_out)).grid(row=1, column=2)

    mode_var = StringVar(window)
    mode_var.set('rmsd')  # Valor por defecto
    Label(window, text="Choose mode:").grid(row=2, sticky='W')
    OptionMenu(window, mode_var, 'rmsd', 'tm_score', 'ratio').grid(row=2, column=1, sticky='W')

    Button(window, text="Execute", command=lambda: execute(entry_in, entry_out, mode_var)).grid(row=3, column=0, columnspan=3)

    window.mainloop()

if __name__ == "__main__":
    main()
