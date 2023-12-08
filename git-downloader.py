import PySimpleGUI as sg
from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import threading
import json

REPO_PATH = 'https://github.com/Birphon/smart-breeder-files.git'
CONFIG_FILE = 'config.json'

class GitFolderWatcher(FileSystemEventHandler):
    def __init__(self, repo_path, local_path):
        self.repo_path = repo_path
        self.local_path = local_path

    def on_modified(self, event):
        if event.src_path.endswith(self.local_path):
            print(f"Change detected in {self.local_path}. Pulling changes...")
            self.pull_changes()

    def pull_changes(self):
        repo = Repo(self.repo_path)
        origin = repo.remote(name='origin')
        origin.pull()

def set_downloads_folder():
    sg.theme('LightBlue2')
    layout = [
        [sg.Text('Enter the path of the "downloads" folder in the GitHub repository:')],
        [sg.InputText(key='folder_path'), sg.FolderBrowse()],
        [sg.Button('Set Folder'), sg.Button('Exit')]
    ]

    window = sg.Window('Set Downloads Folder', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Set Folder':
            folder_path = values['folder_path']
            if folder_path:
                window.close()
                save_config(folder_path)
                return folder_path

    window.close()
    return None

def save_config(folder_path):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump({'downloads_folder': folder_path}, config_file)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
            return config.get('downloads_folder', None)
    return None

def main():
    # Try loading the last used folder from the config
    last_used_folder = load_config()

    # If the folder is not found or new-folder command is provided, set the downloads folder via GUI
    if not last_used_folder or (len(os.sys.argv) > 1 and os.sys.argv[1] == 'new-folder'):
        last_used_folder = set_downloads_folder()
        if not last_used_folder:
            print("Downloads folder not selected. Exiting.")
            return

    # Initialize Git folder watcher
    watcher = GitFolderWatcher(REPO_PATH, last_used_folder)

    # Start the watchdog observer in a separate thread
    observer = Observer()
    observer.schedule(watcher, last_used_folder, recursive=True)
    observer.start()

    try:
        print(f"Watching for changes in {last_used_folder}. Press Ctrl+C to exit.")
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    main()
