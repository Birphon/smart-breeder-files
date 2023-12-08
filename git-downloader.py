import PySimpleGUI as sg
from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import threading


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
                return folder_path

    window.close()
    return None

def main():
    repo_path = 'https://github.com/Birphon/smart-breeder-files.git'
    
    # Set the initial downloads folder via GUI
    downloads_folder = set_downloads_folder()
    if not downloads_folder:
        print("Downloads folder not selected. Exiting.")
        return

    # Initialize Git folder watcher
    watcher = GitFolderWatcher(repo_path, downloads_folder)

    # Start the watchdog observer in a separate thread
    observer = Observer()
    observer.schedule(watcher, downloads_folder, recursive=True)
    observer.start()

    try:
        print(f"Watching for changes in {downloads_folder}. Press Ctrl+C to exit.")
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    main()

