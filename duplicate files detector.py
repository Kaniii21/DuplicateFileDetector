import os
import hashlib
import tkinter as tk
from tkinter import filedialog

class DuplicateFileDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate File Detector")
        self.file_paths = []
        
        # GUI components
        self.label = tk.Label(root, text="Select a folder to scan for duplicates:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=10)

        self.scan_button = tk.Button(root, text="Scan for Duplicates", command=self.scan_duplicates)
        self.scan_button.pack(pady=10)

        self.delete_button = tk.Button(root, text="Delete Duplicates", command=self.delete_duplicates, state=tk.DISABLED)
        self.delete_button.pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.file_paths = self.get_all_files(folder_selected)
            self.scan_button["state"] = tk.NORMAL

    def get_all_files(self, folder):
        file_paths = []
        for root_folder, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root_folder, file)
                file_paths.append(file_path)
        return file_paths

    def get_file_hash(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def scan_duplicates(self):
        hash_dict = {}
        duplicate_files = []

        for file_path in self.file_paths:
            file_hash = self.get_file_hash(file_path)

            if file_hash in hash_dict:
                duplicate_files.append((file_path, hash_dict[file_hash]))
            else:
                hash_dict[file_hash] = file_path

        if duplicate_files:
            self.display_duplicate_files(duplicate_files)
            self.delete_button["state"] = tk.NORMAL
        else:
            tk.messagebox.showinfo("Duplicate File Detector", "No duplicate files found.")

    def display_duplicate_files(self, duplicate_files):
        result_window = tk.Toplevel(self.root)
        result_window.title("Duplicate Files")

        label = tk.Label(result_window, text="Duplicate Files:")
        label.pack(pady=10)

        for file_pair in duplicate_files:
            label_text = f"{file_pair[0]}\n{file_pair[1]}\n{'='*50}"
            tk.Label(result_window, text=label_text).pack()

    def delete_duplicates(self):
        for file_pair in self.duplicate_files:
            os.remove(file_pair[0])

        tk.messagebox.showinfo("Duplicate File Detector", "Duplicate files deleted successfully.")
        self.scan_button["state"] = tk.DISABLED
        self.delete_button["state"] = tk.DISABLED

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFileDetector(root)
    root.mainloop()
