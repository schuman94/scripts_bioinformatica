import tkinter as tk
from tkinter import filedialog, messagebox

def extract_identifiers_from_tsv(tsv_file):
    identifiers = []
    with open(tsv_file, 'r') as f:
        next(f)  # Saltar la primera línea (encabezado)
        for line in f:
            parts = line.strip().split('\t')  # Dividir la línea por la tabulación
            if parts:  # Comprobar si hay al menos una columna
                identifiers.append(parts[0])  # Agregar el primer elemento (primer columna) a la lista de identificadores
    return identifiers

def save_identifiers_to_txt(identifiers, output_file):
    with open(output_file, 'w') as f:
        for identifier in identifiers:
            f.write(f'{identifier}\n')

def browse_tsv_file(entry):
    tsv_file = filedialog.askopenfilename(filetypes=[("TSV files", "*.tsv")])
    entry.delete(0, tk.END)
    entry.insert(0, tsv_file)

def browse_output_file(entry):
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    entry.delete(0, tk.END)
    entry.insert(0, output_file)

def execute_extraction(tsv_file_entry, output_file_entry):
    tsv_file = tsv_file_entry.get()
    output_file = output_file_entry.get()

    if not tsv_file or not output_file:
        messagebox.showerror("Error", "Por favor, seleccione un archivo TSV y un archivo de salida.")
        return

    identifiers = extract_identifiers_from_tsv(tsv_file)
    save_identifiers_to_txt(identifiers, output_file)

    messagebox.showinfo("Éxito", f"Los identificadores se han guardado en {output_file}")

def main():
    root = tk.Tk()
    root.title("Extract Identifiers from TSV")

    # Etiquetas y entradas
    tk.Label(root, text="Archivo TSV").grid(row=0, column=0, sticky=tk.W)
    tsv_file_entry = tk.Entry(root, width=50)
    tsv_file_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_tsv_file(tsv_file_entry)).grid(row=0, column=2)

    tk.Label(root, text="Archivo de salida (TXT)").grid(row=1, column=0, sticky=tk.W)
    output_file_entry = tk.Entry(root, width=50)
    output_file_entry.grid(row=1, column=1)
    tk.Button(root, text="Guardar como", command=lambda: browse_output_file(output_file_entry)).grid(row=1, column=2)

    # Botón de ejecución
    tk.Button(root, text="Extract", command=lambda: execute_extraction(tsv_file_entry, output_file_entry)).grid(row=2, column=0, columnspan=3)

    # Mantener la ventana abierta
    root.mainloop()

if __name__ == '__main__':
    main()
