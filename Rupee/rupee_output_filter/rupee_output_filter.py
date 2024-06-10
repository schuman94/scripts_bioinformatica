import os
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime

def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def browse_input_directory():
    directory = filedialog.askdirectory()
    input_path_var.set(directory)

def browse_output_directory():
    directory = filedialog.askdirectory()
    output_path_var.set(directory)

def browse_log_directory():
    directory = filedialog.askdirectory()
    log_path_var.set(directory)

def check_empty_files(directory, log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write("Rupee no ha podido analizar correctamente los siguientes péptidos, por lo que han sido descartados:\n")
        for file_name in os.listdir(directory):
            if file_name.endswith(".txt"):
                file_path = convertir_a_ruta_larga(os.path.join(directory, file_name))
                with open(file_path, "r") as input_file:
                    lines = input_file.readlines()
                # Checking both completely empty files and files with only header
                if len(lines) <= 1:
                    # Getting the base file name by removing the "-output.txt" suffix
                    base_file_name = file_name.replace("-output.txt", "")
                    log_file.write(f"{base_file_name}\n")
                elif similarity_mode_var.get():
                    # Searching for the line where the peptide is compared with itself
                    base_file_name = file_name.replace("-output.txt", "")
                    for line in lines[1:]:
                        fields = line.split(",")
                        if fields[1] == base_file_name and fields[2] == base_file_name:
                            # Checking if the comparison is exact
                            if fields[3] == "0" and fields[4] == "0000" and fields[5] == "1":
                                break
                    else:   # Este else está asociado el bucle for, de modo que solo se ejecuta si el bucle for se ha ejecutado entero
                            # sin haberse roto con un break, es decir, si no se ha encontrado una linea
                            # que compare al peptido consigo mismo con un 100% de similitud
                        # If no exact comparison was found, log the file as invalid
                        log_file.write(f"{base_file_name}\n")

def get_invalid_file_names(log_file_path):
    with open(log_file_path, 'r') as log_file:
        # Skip the first line
        next(log_file)
        invalid_file_names = [line.strip() for line in log_file]
    return invalid_file_names

def process_files():
    input_directory = convertir_a_ruta_larga(input_path_var.get())
    output_directory = convertir_a_ruta_larga(output_path_var.get())

    max_field_4_value = max_field_4_var.get()
    min_field_5_value = min_field_5_var.get()

    log_directory = convertir_a_ruta_larga(log_path_var.get()) # Ruta al directorio donde se guardará el fichero log"
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    # A la ruta del directorio le añadimos el nombre del fichero log
    log_file_path = convertir_a_ruta_larga(os.path.join(log_directory, f"rupee_log_{formatted_time}.txt"))

    if not input_directory or not output_directory or not log_directory:
        messagebox.showerror("Error", "Please, select both input, output, and log directories.")
        return

    if similarity_mode_var.get() and ((max_field_4_var.get() != "" or min_field_5_var.get() != "")):
        messagebox.showerror("Error", "To execute the similarity matrix mode, max rmsd and min tmscore fields must be empty.")
        return

    check_empty_files(input_directory, log_file_path)  # Check and log empty files
    invalid_file_names = get_invalid_file_names(log_file_path)

    txt_files = [f for f in os.listdir(input_directory) if f.endswith(".txt") and os.path.getsize(os.path.join(input_directory, f)) > 0]

    if not txt_files:
        messagebox.showerror("Error", "No .txt files found in the input directory.")
        return

    for file in txt_files:
        input_file_path = convertir_a_ruta_larga(os.path.join(input_directory, file))

        # Get the base file name by removing the extension and the "-output.txt" suffix
        file_name_without_output_ext = os.path.splitext(file)[0].replace("-output", "")

        if file_name_without_output_ext in invalid_file_names:
            continue

        with open(input_file_path, "r") as input_file:
            lines = input_file.readlines()

        # Modifying the output file name
        max_field = max_field_4_var.get()
        min_field = min_field_5_var.get()

        # Inicializamos el nombre del archivo
        new_file_name = f"{file_name_without_output_ext}-filtered"

        # Agregamos los campos si no están vacíos
        if max_field:
            new_file_name += f"_{max_field}"
        if min_field:
            new_file_name += f"_{min_field}"

        new_file_name += ".txt"

        output_file_path = convertir_a_ruta_larga(os.path.join(output_directory, new_file_name))

        header = lines[0]
        data_lines = lines[1:]

        filtered_lines = [header]
        line_number = 1

        for line in data_lines:
            # Replace the 4th and 6th comma with a dot
            count = 0
            modified_line = ""
            for char in line:
                if char == ",":
                    count += 1
                    if count in [4, 6]:
                        char = "."
                modified_line += char

            fields = modified_line.strip().split(",")

            field_4_value = float(fields[3])
            field_5_value = float(fields[4])

            filter_pass = True

            # Only apply the filter if a value has been provided
            if max_field_4_value != "":
                max_field_4_value = float(max_field_4_value)
                if field_4_value > max_field_4_value:
                    filter_pass = False

            # Only apply the filter if a value has been provided
            if min_field_5_value != "":
                min_field_5_value = float(min_field_5_value)
                if field_5_value < min_field_5_value:
                    filter_pass = False

            if filter_pass:
                new_line = f"{line_number},{','.join(fields[1:])}\n"
                filtered_lines.append(new_line)
                line_number += 1

        if len(filtered_lines) > 1:
            with open(output_file_path, "w") as output_file:
                output_file.writelines(filtered_lines)

    # Final step: Remove lines from output files that match invalid file names
    output_files = [f for f in os.listdir(output_directory) if f.endswith(".txt")]

    for file in output_files:
        output_file_path = convertir_a_ruta_larga(os.path.join(output_directory, file))
        with open(output_file_path, "r") as output_file:
            lines = output_file.readlines()
        # Filter out lines that contain any of the invalid file names
        filtered_lines = [line for line in lines if not any(invalid_name in line for invalid_name in invalid_file_names)]
        with open(output_file_path, "w") as output_file:
            output_file.writelines(filtered_lines)

    messagebox.showinfo("Success", "Files have been processed and saved in the output directory.")

app = tk.Tk()
app.title("Rupee output files processor")

for i in range(4):
    app.columnconfigure(i, weight=1, minsize=100)
    app.rowconfigure(i, weight=1, minsize=50)

input_label = tk.Label(app, text="Input Directory:")
input_label.grid(column=0, row=0, sticky="e", padx=5, pady=5)

input_path_var = tk.StringVar()
input_entry = tk.Entry(app, textvariable=input_path_var, width=40)
input_entry.grid(column=1, row=0, columnspan=2, sticky="ew", padx=5, pady=5)

browse_input_button = tk.Button(app, text="Browse", command=browse_input_directory)
browse_input_button.grid(column=3, row=0, sticky="w", padx=5, pady=5)

output_label = tk.Label(app, text="Output Directory:")
output_label.grid(column=0, row=1, sticky="e", padx=5, pady=5)

output_path_var = tk.StringVar()
output_entry = tk.Entry(app, textvariable=output_path_var, width=40)
output_entry.grid(column=1, row=1, columnspan=2, sticky="ew", padx=5, pady=5)

browse_output_button = tk.Button(app, text="Browse", command=browse_output_directory)
browse_output_button.grid(column=3, row=1, sticky="w", padx=5, pady=5)

max_field_4_label = tk.Label(app, text="Max rmsd:")
max_field_4_label.grid(column=0, row=2, sticky="e", padx=5, pady=5)

max_field_4_var = tk.StringVar()
max_field_4_entry = tk.Entry(app, textvariable=max_field_4_var, width=10)
max_field_4_entry.grid(column=1, row=2, sticky="w", padx=5, pady=5)

min_field_5_label = tk.Label(app, text="Min tm_score:")
min_field_5_label.grid(column=0, row=3, sticky="e", padx=5, pady=5)

min_field_5_var = tk.StringVar()
min_field_5_entry = tk.Entry(app, textvariable=min_field_5_var, width=10)
min_field_5_entry.grid(column=1, row=3, sticky="w", padx=5, pady=5)

log_label = tk.Label(app, text="Log Directory:")
log_label.grid(column=0, row=4, sticky="e", padx=5, pady=5)

log_path_var = tk.StringVar()
log_entry = tk.Entry(app, textvariable=log_path_var, width=40)
log_entry.grid(column=1, row=4, columnspan=2, sticky="ew", padx=5, pady=5)

browse_log_button = tk.Button(app, text="Browse", command=browse_log_directory)
browse_log_button.grid(column=3, row=4, sticky="w", padx=5, pady=5)

similarity_mode_var = tk.IntVar()
similarity_mode_check = tk.Checkbutton(app, text="Similarity matrix mode", variable=similarity_mode_var)
similarity_mode_check.grid(column=1, row=5, columnspan=2, padx=5, pady=5)

process_button = tk.Button(app, text="Execute", command=process_files)
process_button.grid(column=1, row=6, columnspan=2, padx=5, pady=5)

app.mainloop()
