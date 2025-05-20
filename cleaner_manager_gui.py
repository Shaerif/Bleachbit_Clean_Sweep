import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class CleanerManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('BleachBit Cleaner Manager')
        self.create_widgets()

    def create_widgets(self):
        self.add_button = tk.Button(self.root, text='Add Cleaner', command=self.add_cleaner)
        self.add_button.pack(pady=10)

        self.remove_button = tk.Button(self.root, text='Remove Cleaner', command=self.remove_cleaner)
        self.remove_button.pack(pady=10)

        self.list_button = tk.Button(self.root, text='List Cleaners', command=self.list_cleaners)
        self.list_button.pack(pady=10)

    def add_cleaner(self):
        file_path = filedialog.askopenfilename(filetypes=[('XML Files', '*.xml')])
        if file_path:
            target_dir = os.path.join(os.getenv('APPDATA'), 'BleachBit', 'cleaners')
            os.makedirs(target_dir, exist_ok=True)
            shutil.copy(file_path, target_dir)
            messagebox.showinfo('Success', 'Cleaner added successfully!')

    def remove_cleaner(self):
        file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getenv('APPDATA'), 'BleachBit', 'cleaners'), filetypes=[('XML Files', '*.xml')])
        if file_path:
            os.remove(file_path)
            messagebox.showinfo('Success', 'Cleaner removed successfully!')

    def list_cleaners(self):
        cleaners_dir = os.path.join(os.getenv('APPDATA'), 'BleachBit', 'cleaners')
        cleaners = os.listdir(cleaners_dir) if os.path.exists(cleaners_dir) else []
        messagebox.showinfo('Cleaners', '\n'.join(cleaners) if cleaners else 'No cleaners found.')

if __name__ == '__main__':
    root = tk.Tk()
    app = CleanerManagerGUI(root)
    root.mainloop()