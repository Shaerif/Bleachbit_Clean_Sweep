#!/usr/bin/env python3

import json
import os
import shutil
import datetime
from pathlib import Path

class BleachBitSettingsManager:
    def __init__(self):
        # Get BleachBit config directory
        self.config_dir = os.path.join(os.getenv('APPDATA'), 'BleachBit') if os.name == 'nt' else \
                         os.path.expanduser('~/.config/bleachbit')
        
        # Ensure backup directory exists
        self.backup_dir = os.path.join(self.config_dir, 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Define important files to backup
        self.important_files = [
            'bleachbit.ini',  # Main settings file
            'memory.json',    # Memory of cleaned files
            'whitelist.json', # Whitelist settings
            'cleaners'        # Custom cleaners directory
        ]
    
    def create_backup(self, backup_name=None):
        """Create a backup of BleachBit settings and configurations."""
        if not backup_name:
            backup_name = f'bleachbit_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        os.makedirs(backup_path, exist_ok=True)
        
        for item in self.important_files:
            src = os.path.join(self.config_dir, item)
            dst = os.path.join(backup_path, item)
            
            if os.path.exists(src):
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
        
        # Create metadata file
        metadata = {
            'backup_date': datetime.datetime.now().isoformat(),
            'backup_items': self.important_files
        }
        
        with open(os.path.join(backup_path, 'backup_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=4)
        
        return backup_path
    
    def restore_backup(self, backup_name):
        """Restore BleachBit settings from a backup."""
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f'Backup {backup_name} not found')
        
        # Verify backup integrity
        metadata_file = os.path.join(backup_path, 'backup_metadata.json')
        if not os.path.exists(metadata_file):
            raise ValueError('Invalid backup: missing metadata file')
        
        # Create a backup before restoring
        self.create_backup('pre_restore_backup')
        
        # Restore files
        for item in self.important_files:
            src = os.path.join(backup_path, item)
            dst = os.path.join(self.config_dir, item)
            
            if os.path.exists(src):
                if os.path.isdir(src):
                    shutil.rmtree(dst, ignore_errors=True)
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
    
    def list_backups(self):
        """List all available backups."""
        backups = []
        for item in os.listdir(self.backup_dir):
            metadata_file = os.path.join(self.backup_dir, item, 'backup_metadata.json')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                backups.append({
                    'name': item,
                    'date': metadata['backup_date'],
                    'items': metadata['backup_items']
                })
        return backups
    
    def export_checked_options(self, export_file):
        """Export currently checked cleaning options to a file."""
        config_file = os.path.join(self.config_dir, 'bleachbit.ini')
        if not os.path.exists(config_file):
            raise FileNotFoundError('BleachBit configuration file not found')
        
        # Read current configuration
        with open(config_file, 'r') as f:
            config_data = f.read()
        
        # Export to specified file
        with open(export_file, 'w') as f:
            f.write(config_data)
    
    def import_checked_options(self, import_file):
        """Import cleaning options from a file."""
        if not os.path.exists(import_file):
            raise FileNotFoundError(f'Import file {import_file} not found')
        
        config_file = os.path.join(self.config_dir, 'bleachbit.ini')
        
        # Backup current configuration
        if os.path.exists(config_file):
            self.create_backup('pre_import_backup')
        
        # Import configuration
        shutil.copy2(import_file, config_file)

def main():
    manager = BleachBitSettingsManager()
    
    # Example usage
    try:
        # Create a backup
        backup_path = manager.create_backup()
        print(f'Created backup at: {backup_path}')
        
        # List available backups
        backups = manager.list_backups()
        print('\nAvailable backups:')
        for backup in backups:
            print(f"- {backup['name']} (created: {backup['date']})")
        
        # Export current options
        export_file = os.path.join(os.path.dirname(__file__), 'bleachbit_options.cfg')
        manager.export_checked_options(export_file)
        print(f'\nExported options to: {export_file}')
        
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    main()