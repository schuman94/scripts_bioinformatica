import os
import requests
import tkinter as tk
from tkinter import filedialog

def read_urls(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

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
            failed_downloads.append(url)
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

def browse_urls_file():
    urls_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return urls_file

def browse_destination_folder():
    destination_folder = filedialog.askdirectory()
    return destination_folder

def main():
    root = tk.Tk()
    root.withdraw()

    urls_file = browse_urls_file()
    if not urls_file:
        print("No se seleccionó ningún archivo de enlaces.")
        return

    destination_folder = browse_destination_folder()
    if not destination_folder:
        print("No se seleccionó ninguna carpeta de destino.")
        return

    url_list = read_urls(urls_file)
    download_files(url_list, destination_folder)

if __name__ == '__main__':
    main()
