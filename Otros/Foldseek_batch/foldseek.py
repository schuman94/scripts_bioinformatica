import os
import requests
import sys
import time
import tarfile
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def convertir_a_ruta_larga(ruta):
    if os.name == 'nt':
        ruta = os.path.abspath(ruta)
        if not ruta.startswith('\\\\?\\'):
            ruta = '\\\\?\\' + ruta
    return ruta

def foldseek_search(file_path, database, mode):
    url = 'https://search.foldseek.com/api/ticket'

    files = {'q': open(file_path, 'rb')}
    data = {'mode': mode, 'database[]': database}

    print(f'Processing {file_path}...')

    while True:
        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            return response.json()['id']
        elif response.status_code == 429:
            print('Rate limit reached. Pausing for 5 minutes...')
            time.sleep(300)  # pause for 5 minutes
        else:
            print(f'Error in Foldseek search. Status code: {response.status_code}, Response: {response.text}')
            sys.exit(1)

def check_status(ticket_id):
    url = f'https://search.foldseek.com/api/ticket/{ticket_id}'
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'COMPLETE':
                return ticket_id
            elif data['status'] in ('PENDING', 'RUNNING'):
                print('Task is still pending, waiting for 10 more seconds...')
                time.sleep(10)
            else:
                print('Unknown status:', data['status'])
                return None
        else:
            print('Error checking status:', response.status_code)
            return None

def download_results(ticket_id, output_path, pdb_filename, database, mode):
    url = f'https://search.foldseek.com/api/result/download/{ticket_id}'
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        tar_gz_path = convertir_a_ruta_larga(os.path.join(output_path, f'{pdb_filename}_{database}_{mode}_result.tar.gz'))
        with open(tar_gz_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

        # Decompress the tar file
        with tarfile.open(tar_gz_path, 'r:gz') as tar:
            tar.extractall(output_path)
            tar_contents = tar.getnames()  # Save the names of the files

        # Rename the decompressed file
        original_file = convertir_a_ruta_larga(os.path.join(output_path, tar_contents[0]))  # assumes only one file in tar
        new_file = convertir_a_ruta_larga(os.path.join(output_path, f'{pdb_filename}_{database}.{mode}'))
        os.rename(original_file, new_file)

        print(f'Results for {pdb_filename} downloaded and renamed.')

        # Remove the .tar.gz file
        os.remove(tar_gz_path)

        # Check if the new file is empty, if so, delete it
        if not check_and_delete_empty_files(new_file):

            # Format the file based on the mode
            format_results(new_file, mode)
    else:
        print('Error downloading results:', response.status_code)

def check_and_delete_empty_files(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if len(lines) == 0:  # if file is empty
        os.remove(file_path)
        print(f'File {file_path} was empty and has been deleted.')
        return True  # file was empty

    return False  # file was not empty

def format_results(file_path, mode):
    output_path = file_path.replace('.' + mode, '.tsv')
    with open(file_path, 'r') as input_file, open(output_path, 'w') as output_file:
        column_name = "TM-score" if mode == "tmalign" else "E-Value"
        output_file.write(f"Target\tScientific Name\t{column_name}\tSeq. Id\tScore\tQuery aligned\tTarget aligned\tTarget seq.\n")
        for line in input_file:
            columns = line.split('\t')

            target = columns[1]
            seq_id = columns[2]
            metric_score = columns[11]
            score = columns[12]
            query_aligned = columns[15]
            target_aligned = columns[16]
            target_seq = columns[18]
            scientific_name = columns[20].rstrip()  # remove newline at the end

            output_file.write(f"{target}\t{scientific_name}\t{metric_score}\t{seq_id}\t{score}\t{query_aligned}\t{target_aligned}\t{target_seq}\n")

    # Now call the modify_tsv function on the new file
    modify_tsv(output_path, mode)

    print(f'Formatted results saved in {output_path}.')
    os.remove(file_path)

def modify_tsv(file_path, mode):
    # Load the TSV into a pandas DataFrame
    df = pd.read_csv(file_path, sep='\t')

    # Split the first column and expand into new dataframe
    new_cols = df['Target'].str.split(' ', n=1, expand=True)

    # Create new columns in the original dataframe
    df['New_target'] = new_cols[0]
    df['Description'] = new_cols[1]

    # Create new URL column
    df['URL'] = 'https://www.alphafold.ebi.ac.uk/entry/' + df['New_target'].str.replace(r'-F\d+-model_v4', '', regex=True)

    df['Target'] = df['New_target']

    # Reorder the dataframe columns
    df = df[['URL', 'Target', 'Description'] + [col for col in df.columns if col not in ['URL', 'Target', 'Description', 'New_target']]]

    # Save the DataFrame back into a TSV
    #df.to_csv(file_path, sep='\t', index=False)

    # Save the DataFrame into an Excel file
    excel_file_path = convertir_a_ruta_larga(file_path.replace('.tsv', f'_{mode}.xlsx'))
    df.to_excel(excel_file_path, index=False)

    # Remove the TSV file
    os.remove(file_path)

# Y ahora agregamos la interfaz gráfica en lugar de obtener los argumentos de la línea de comandos
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=20, pady=20)

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.mode = tk.StringVar(value="tmalign")
        self.database = tk.StringVar(value="afdb-swissprot")

        self.create_widgets()

    def create_widgets(self):
        # Input directory
        self.input_dir_label = tk.Label(self, text="Input Directory:")
        self.input_dir_label.grid(row=0, column=0, sticky="w")  # position in grid
        self.input_dir_entry = tk.Entry(self, textvariable=self.input_dir, width=50)  # Add width option here
        self.input_dir_entry.grid(row=0, column=1, sticky="w")  # position in grid
        self.input_dir_button = tk.Button(self, text="Browse...", command=self.select_input_dir)
        self.input_dir_button.grid(row=0, column=2, sticky="w")  # position in grid

        # Output directory
        self.output_dir_label = tk.Label(self, text="Output Directory:")
        self.output_dir_label.grid(row=1, column=0, sticky="w")  # position in grid
        self.output_dir_entry = tk.Entry(self, textvariable=self.output_dir, width=50)  # Add width option here
        self.output_dir_entry.grid(row=1, column=1, sticky="w")  # position in grid
        self.output_dir_button = tk.Button(self, text="Browse...", command=self.select_output_dir)
        self.output_dir_button.grid(row=1, column=2, sticky="w")  # position in grid

        # Mode
        self.mode_label = tk.Label(self, text="Mode:")
        self.mode_label.grid(row=2, column=0, sticky="w")  # position in grid
        self.mode_option = ttk.Combobox(self, textvariable=self.mode, values=("3diaa", "tmalign"))
        self.mode_option.grid(row=2, column=1, sticky="w")  # position in grid

        # Database
        self.database_label = tk.Label(self, text="Database:")
        self.database_label.grid(row=3, column=0, sticky="w")  # position in grid
        self.database_option = ttk.Combobox(self, textvariable=self.database, values=("afdb-swissprot", "afdb50", "afdb-proteome"))
        self.database_option.grid(row=3, column=1, sticky="w")  # position in grid

        # Execute button
        self.execute_button = tk.Button(self, text="Execute", command=self.execute_foldseek)
        self.execute_button.grid(row=4, column=1, columnspan=2, sticky="w")  # position in grid

        # Configure the column spacing
        self.grid_columnconfigure(0, pad=50)  # adjust the pad value as necessary
        self.grid_columnconfigure(1, pad=50)  # adjust the pad value as necessary
        self.grid_columnconfigure(2, pad=50)  # adjust the pad value as necessary

        # Configure the row spacing
        self.grid_rowconfigure(0, pad=20)  # adjust the pad value as necessary
        self.grid_rowconfigure(1, pad=20)  # adjust the pad value as necessary
        self.grid_rowconfigure(2, pad=20)  # adjust the pad value as necessary
        self.grid_rowconfigure(3, pad=20)  # adjust the pad value as necessary
        self.grid_rowconfigure(4, pad=20)  # adjust the pad value as necessary

    def select_input_dir(self):
        filename = filedialog.askdirectory()
        self.input_dir.set(filename)

    def select_output_dir(self):
        filename = filedialog.askdirectory()
        self.output_dir.set(filename)

    def execute_foldseek(self):
        input_dir = convertir_a_ruta_larga(self.input_dir.get())
        output_dir = convertir_a_ruta_larga(self.output_dir.get())
        mode = self.mode.get()
        database = self.database.get()

        # Iterate over all pdb files in the directory
        for pdb_filename in os.listdir(input_dir):
            if pdb_filename.endswith(".pdb"):
                pdb_file_path = convertir_a_ruta_larga(os.path.join(input_dir, pdb_filename))
                ticket_id = foldseek_search(pdb_file_path, database, mode)
                if ticket_id is not None:
                    ticket_id = check_status(ticket_id)
                    if ticket_id is not None:
                        download_results(ticket_id, output_dir, os.path.splitext(pdb_filename)[0], database, mode)
                else:
                    print('Error in Foldseek search.')

        messagebox.showinfo("Information", "The process has finished")

root = tk.Tk()
root.title("Foldseek")
root.geometry("610x250")  # Set the window size (width x height)
app = Application(master=root)
app.mainloop()
