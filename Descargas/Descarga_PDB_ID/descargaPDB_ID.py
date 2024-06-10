import os
import requests
import tkinter as tk
from tkinter import filedialog

def read_identifiers(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

def build_urls(identifiers):
    base_url = "https://alphafold.ebi.ac.uk/files/AF-{}-F1-model_v4.pdb"
    return [base_url.format(identifier) for identifier in identifiers]

def download_files(url_list, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    failed_downloads = []

    for url in url_list:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {url}: {e}")
            identifier = os.path.basename(url).split('-')[1]
            failed_downloads.append(f"https://www.uniprot.org/uniprotkb/{identifier}/entry")
            continue

        file_name = os.path.basename(url)
        file_path = os.path.join(destination_folder, file_name)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"Descargado: {file_path}")

    if failed_downloads:
        with open(os.path.join(destination_folder, 'failed_downloads.txt'), 'w') as f:
            for failed_url in failed_downloads:
                f.write(f"{failed_url}\n")
        print(f"Los enlaces fallidos se han guardado en {os.path.join(destination_folder, 'failed_downloads.txt')}")

def browse_identifiers_file():
    identifiers_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return identifiers_file

def browse_destination_folder():
    destination_folder = filedialog.askdirectory()
    return destination_folder

def main():
    root = tk.Tk()
    root.withdraw()

    identifiers_file = browse_identifiers_file()
    if not identifiers_file:
        print("No se seleccionó ningún archivo de identificadores.")
        return

    destination_folder = browse_destination_folder()
    if not destination_folder:
        print("No se seleccionó ninguna carpeta de destino.")
        return

    identifiers = read_identifiers(identifiers_file)
    url_list = build_urls(identifiers)
    download_files(url_list, destination_folder)

if __name__ == '__main__':
    main()
