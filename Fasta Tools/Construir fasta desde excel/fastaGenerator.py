import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

class FastaGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FASTA Generator")

        # Variables
        self.filepath = None
        self.header = tk.BooleanVar(value=False)

        # Labels and buttons
        self.label = tk.Label(root, text="Select file:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.file_button = tk.Button(root, text="Browse", command=self.load_file)
        self.file_button.grid(row=0, column=1, padx=10, pady=10)

        self.header_check = tk.Checkbutton(root, text="First row is header", variable=self.header)
        self.header_check.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.id_label = tk.Label(root, text="Column for ID (A, B, C...):")
        self.id_label.grid(row=2, column=0, padx=10, pady=10)

        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=2, column=1, padx=10, pady=10)

        self.seq_label = tk.Label(root, text="Columns for sequence (comma separated, A, B, C...):")
        self.seq_label.grid(row=3, column=0, padx=10, pady=10)

        self.seq_entry = tk.Entry(root)
        self.seq_entry.grid(row=3, column=1, padx=10, pady=10)

        self.desc_label = tk.Label(root, text="Columns for description (optional, comma separated, A, B, C...):")
        self.desc_label.grid(row=4, column=0, padx=10, pady=10)

        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=4, column=1, padx=10, pady=10)

        self.generate_button = tk.Button(root, text="Generate FASTA", command=self.generate_fasta)
        self.generate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

    def load_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xlsm"), ("CSV files", "*.csv"), ("TSV files", "*.tsv")])
        if self.filepath:
            messagebox.showinfo("File selected", f"Selected file: {self.filepath}")

    def letter_to_index(self, letter):
        """Convierte una letra (A, B, C...) en un índice de columna basado en 0"""
        return ord(letter.lower()) - ord('a')

    def generate_fasta(self):
        if not self.filepath:
            messagebox.showerror("Error", "No file selected")
            return

        # Load file into pandas dataframe
        try:
            if self.filepath.endswith(('.xlsx', '.xlsm')):
                df = pd.read_excel(self.filepath, header=0 if self.header.get() else None)
            elif self.filepath.endswith('.csv'):
                df = pd.read_csv(self.filepath, header=0 if self.header.get() else None)
            elif self.filepath.endswith('.tsv'):
                df = pd.read_csv(self.filepath, delimiter='\t', header=0 if self.header.get() else None)
            else:
                messagebox.showerror("Error", "Unsupported file format")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            return

        # Get column selections using letters
        try:
            id_col = self.letter_to_index(self.id_entry.get())  # Convierte letra a índice
            seq_cols = [self.letter_to_index(x.strip()) for x in self.seq_entry.get().split(',')]  # Convierte letras a índices
            desc_cols = [self.letter_to_index(x.strip()) for x in self.desc_entry.get().split(',')] if self.desc_entry.get() else []
        except ValueError:
            messagebox.showerror("Error", "Invalid column input")
            return

        # Generate FASTA records
        fasta_records = []
        for index, row in df.iterrows():
            # ID and description
            id_value = str(row[id_col])
            desc_value = " ".join([str(row[col]) for col in desc_cols]) if desc_cols else ""
            full_id = f"{id_value} {desc_value}".strip()

            # Eliminar el ">" si ya está presente
            if full_id.startswith(">"):
                full_id = full_id[1:].strip()

            # Sequence
            seq_value = "".join([str(row[col]) for col in seq_cols if pd.notna(row[col])])

            # Create SeqRecord
            record = SeqRecord(Seq(seq_value), id=full_id, description="")
            fasta_records.append(record)

        # Save to FASTA file
        output_path = filedialog.asksaveasfilename(defaultextension=".fasta", filetypes=[("FASTA files", "*.fasta")])
        if output_path:
            with open(output_path, "w") as fasta_file:
                SeqIO.write(fasta_records, fasta_file, "fasta-2line")
            messagebox.showinfo("Success", f"FASTA file saved: {output_path}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FastaGeneratorApp(root)
    root.mainloop()
