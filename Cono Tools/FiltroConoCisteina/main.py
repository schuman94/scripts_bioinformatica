import tkinter as tk
from tkinter import messagebox
import file_utils

def filtrar_secuencias():
    input_file = entrada_var.get()
    output_folder = salida_var.get()
    filter_option = patron_var.get()
    gap1 = None if not gap1_var.get() else int(gap1_var.get())
    gap2 = None if not gap2_var.get() else int(gap2_var.get())
    num_c = None if not num_c_var.get() else int(num_c_var.get())

    if not input_file or not output_folder:
        messagebox.showerror("Error", "Selecciona un archivo de entrada y una carpeta de salida")
        return

    def run_filtering():
        nonlocal progress_window
        file_utils.filtrar_secuencias(input_file, output_folder, filter_option, gap1, gap2, num_c)
        progress_window.destroy()
        messagebox.showinfo("Éxito", "El filtrado de secuencias se ha completado")

    progress_window = tk.Toplevel(ventana)
    progress_window.title("Filtrando secuencias")
    progress_window.geometry("250x100")
    tk.Label(progress_window, text="Filtrando secuencias, por favor espera...").pack(pady=10)
    ventana.after(100, run_filtering)

ventana = tk.Tk()
ventana.title("Filtrado de secuencias FASTA")
ventana.minsize(600, 180)

entrada_var = tk.StringVar()
salida_var = tk.StringVar()
patron_var = tk.StringVar()
gap1_var = tk.StringVar()
gap2_var = tk.StringVar()
num_c_var = tk.StringVar()

tk.Label(ventana, text="Archivo de entrada (.fasta):").grid(row=0, column=0, sticky="e")
tk.Entry(ventana, textvariable=entrada_var, width=60).grid(row=0, column=1)
tk.Button(ventana, text="Seleccionar", command=file_utils.seleccionar_archivo(entrada_var)).grid(row=0, column=2)

tk.Label(ventana, text="Carpeta de salida:").grid(row=1, column=0, sticky="e")
tk.Entry(ventana, textvariable=salida_var, width=60).grid(row=1, column=1)
tk.Button(ventana, text="Seleccionar", command=file_utils.seleccionar_carpeta(salida_var)).grid(row=1, column=2)

tk.Label(ventana, text="Patrón de filtrado:").grid(row=2, column=0, sticky="e")
patron_var.set("C")

def update_patron_menu(*args):
    if patron_var.get() == "Patron alfa":
        gap1_entry.grid(row=3, column=1)
        gap2_entry.grid(row=3, column=2)
        num_c_label.grid_remove()
        num_c_entry.grid_remove()
    else:
        gap1_entry.grid_remove()
        gap2_entry.grid_remove()
        num_c_label.grid(row=3, column=0, sticky="e")
        num_c_entry.grid(row=3, column=1)

patron_var.trace("w", update_patron_menu)

tk.OptionMenu(ventana, patron_var, "C", "Patron alfa").grid(row=2, column=1, sticky="w")
gap1_entry = tk.Entry(ventana, textvariable=gap1_var, width=10)
gap2_entry = tk.Entry(ventana, textvariable=gap2_var, width=10)
num_c_label = tk.Label(ventana, text="Número de C:")
num_c_entry = tk.Entry(ventana, textvariable=num_c_var, width=10)

tk.Button(ventana, text="Iniciar filtrado", command=filtrar_secuencias).grid(row=4, column=1, pady=10)

ventana.mainloop()
