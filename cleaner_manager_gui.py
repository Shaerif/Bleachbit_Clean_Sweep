import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import subprocess
from bleachbit_settings_manager import BleachBitSettingsManager

class CleanerManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('BleachBit Cleaner Manager')
        self.debug_mode = tk.BooleanVar()
        self.settings_manager = BleachBitSettingsManager()
        self.create_widgets()

    def create_widgets(self):
        self.add_button = tk.Button(self.root, text='Add Cleaner', command=self.add_cleaner)
        self.add_button.pack(pady=10)

        self.remove_button = tk.Button(self.root, text='Remove Cleaner', command=self.remove_cleaner)
        self.remove_button.pack(pady=10)

        self.list_button = tk.Button(self.root, text='List Cleaners', command=self.list_cleaners)
        self.list_button.pack(pady=10)

        self.update_bleachbit_button = tk.Button(self.root, text='Update BleachBit', command=self.run_bleachbit_updater)
        self.update_bleachbit_button.pack(pady=5) # Reduced pady for checkbox

        # Version selection
        self.version_var = tk.StringVar(value='stable')
        version_frame = tk.Frame(self.root)
        version_frame.pack(pady=5)
        tk.Label(version_frame, text='Select BleachBit Version:').pack(side='left')
        self.version_combo = ttk.Combobox(version_frame, textvariable=self.version_var, values=['stable', 'beta', 'unstable'], state='readonly', width=10)
        self.version_combo.pack(side='left', padx=5)

        self.debug_checkbox = tk.Checkbutton(self.root, text="Enable Updater Debug Mode", variable=self.debug_mode)
        self.debug_checkbox.pack(pady=5)

        # Progress bar for download visualization
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', padx=10, pady=5)

        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=10)

        # Settings Management Frame
        settings_frame = tk.LabelFrame(self.root, text='Settings Management', padx=5, pady=5)
        settings_frame.pack(padx=10, pady=5, fill='x')

        # Backup & Restore
        backup_button = tk.Button(settings_frame, text='Create Backup', command=self.create_backup)
        backup_button.pack(side='left', padx=5)

        restore_button = tk.Button(settings_frame, text='Restore Backup', command=self.restore_backup)
        restore_button.pack(side='left', padx=5)

        # Import & Export
        export_button = tk.Button(settings_frame, text='Export Settings', command=self.export_settings)
        export_button.pack(side='right', padx=5)

        import_button = tk.Button(settings_frame, text='Import Settings', command=self.import_settings)
        import_button.pack(side='right', padx=5)

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

    def run_bleachbit_updater(self):
        """Runs the BleachBit updater script."""
        import threading
        import sys
        current_dir = os.path.dirname(os.path.abspath(__file__))
        updater_script_path = os.path.join(current_dir, "bleachbit_updater.py")

        if not os.path.exists(updater_script_path):
            messagebox.showerror("Error", f"Updater script not found at {updater_script_path}")
            return

        def run_update():
            try:
                # Prepare command with version and debug options
                command_to_run = [sys.executable, updater_script_path, '--version', self.version_var.get()]
                if self.debug_mode.get():
                    command_to_run.append('--debug')
                # Use subprocess and capture output for progress
                process = subprocess.Popen(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                while True:
                    line = process.stdout.readline()
                    if not line:
                        break
                    # Simple progress bar update: look for percentage in output
                    if '%' in line:
                        import re
                        match = re.search(r'(\d+)%', line)
                        if match:
                            percent = int(match.group(1))
                            self.progress_var.set(percent)
                            self.root.update_idletasks()
                    # Show errors/debug in messagebox if needed
                    if 'ERROR' in line or 'Error' in line:
                        messagebox.showerror('Updater Error', line.strip())
                    if 'DEBUG' in line and self.debug_mode.get():
                        print(line.strip())
                process.wait()
                self.progress_var.set(100)
                self.root.update_idletasks()
                messagebox.showinfo("Updater Finished", "BleachBit update/download process completed.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run updater: {e}")
                self.progress_var.set(0)
                self.root.update_idletasks()

        # Run in a thread to avoid blocking the GUI
        threading.Thread(target=run_update, daemon=True).start()

        # Assuming bleachbit_updater.py is in the same directory as this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        updater_script_path = os.path.join(current_dir, "bleachbit_updater.py")

        if not os.path.exists(updater_script_path):
            messagebox.showerror("Error", f"Updater script not found at {updater_script_path}")
            return

        try:
            # For Windows, use 'start' command with 'python' to open in a new console
            # that remains open after the script finishes (due to /k).
            command_to_run = ['python', updater_script_path]
            if self.debug_mode.get():
                command_to_run.append('--debug')

            if os.name == 'nt':
                # Prepend 'start cmd /k' for Windows to keep console open and show output
                full_command = ['start', 'cmd', '/k'] + command_to_run
                subprocess.Popen(full_command, shell=True)
                messagebox.showinfo("Updater Started", "BleachBit updater script has been started in a new window. Please follow the instructions there.")
            else:
                # For Linux/macOS, this is a basic example and might need adjustment.
                # It tries to open in xterm and keep it open.
                try:
                    # For Linux/macOS, construct the command string for xterm
                    # Ensure paths with spaces are quoted if necessary, though updater_script_path should be safe
                    cmd_string = f"{' '.join(['python3'] + command_to_run)}; echo 'Press Enter to close...'; read"
                    subprocess.Popen(['xterm', '-e', cmd_string])
                    messagebox.showinfo("Updater Started", "BleachBit updater script has been started in a new terminal. Please follow the instructions there.")
                except FileNotFoundError:
                    messagebox.showerror("Error", "xterm not found. Please run the updater script manually from a terminal: python3 bleachbit_updater.py")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start updater script: {e}")

    def create_backup(self):
        """Create a backup of BleachBit settings."""
        try:
            backup_path = self.settings_manager.create_backup()
            messagebox.showinfo('Success', f'Backup created successfully at:\n{backup_path}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to create backup: {e}')

    def restore_backup(self):
        """Restore BleachBit settings from a backup."""
        try:
            backups = self.settings_manager.list_backups()
            if not backups:
                messagebox.showinfo('Info', 'No backups available')
                return

            # Create a simple dialog to select a backup
            dialog = tk.Toplevel(self.root)
            dialog.title('Select Backup')
            dialog.geometry('400x300')

            # Create a listbox with scrollbar
            frame = ttk.Frame(dialog)
            frame.pack(fill='both', expand=True, padx=5, pady=5)

            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side='right', fill='y')

            listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
            listbox.pack(side='left', fill='both', expand=True)

            scrollbar.config(command=listbox.yview)

            # Populate the listbox
            for backup in backups:
                listbox.insert('end', f"{backup['name']} - {backup['date']}")

            def do_restore():
                selection = listbox.curselection()
                if selection:
                    backup_name = backups[selection[0]]['name']
                    try:
                        self.settings_manager.restore_backup(backup_name)
                        messagebox.showinfo('Success', 'Settings restored successfully')
                        dialog.destroy()
                    except Exception as e:
                        messagebox.showerror('Error', f'Failed to restore backup: {e}')
                else:
                    messagebox.showwarning('Warning', 'Please select a backup to restore')

            ttk.Button(dialog, text='Restore', command=do_restore).pack(pady=5)
            ttk.Button(dialog, text='Cancel', command=dialog.destroy).pack(pady=5)

        except Exception as e:
            messagebox.showerror('Error', f'Failed to list backups: {e}')

    def export_settings(self):
        """Export BleachBit settings to a file."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension='.cfg',
                filetypes=[('Configuration Files', '*.cfg')],
                title='Export BleachBit Settings'
            )
            if file_path:
                self.settings_manager.export_checked_options(file_path)
                messagebox.showinfo('Success', f'Settings exported successfully to:\n{file_path}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to export settings: {e}')

    def import_settings(self):
        """Import BleachBit settings from a file."""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[('Configuration Files', '*.cfg')],
                title='Import BleachBit Settings'
            )
            if file_path:
                self.settings_manager.import_checked_options(file_path)
                messagebox.showinfo('Success', 'Settings imported successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to import settings: {e}')


if __name__ == '__main__':
    root = tk.Tk()
    app = CleanerManagerGUI(root)
    root.mainloop()