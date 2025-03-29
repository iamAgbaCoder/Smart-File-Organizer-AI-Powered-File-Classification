import os
import shutil
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import colorama
from colorama import Fore, Back, Style

# initialize colorama
colorama.init()

print("")
# print(Fore.GREEN + "Hello World")
# print(Fore.GREEN + Back.WHITE + "HELLO WORLD")
#
# Style.RESET_ALL
# print(Fore.WHITE + Back.GREEN + "Hello World")
# Define folder categories
EXTENSIONS = {
    "Images": [".jpg", ".png", ".gif", ".svg", ".jpeg", ".gif", ".ai", ".bmp"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Audios": [".mp3", ".aac", ".ogg", ".wav", ".flac"],
    "Documents": [".pdf", ".docx", ".txt", ".ico"],
    "Archives": [".zip", ".tar", ".rar", ".7z", ".gz"],
    "Executable & Scripts": [".exe", ".msi", ".sh", ".py", ".bat", ".app", ".apk"],
    "Fonts": [".ttf", ".otf"],
    "Plain Text Files": [".txt", ".csv"],
    "Markup Language Files": [".html", ".xml"],
    "Source Code Files": [".py", ".rb", ".js", ".c", ".java", ".php", ".kt"],
    "Photoshop Files": [".psd"],
    "Subtitls": [".srt"]

}

# Organize files
def organize_file(file_path):
    _, ext = os.path.splitext(file_path)
    print(file_path)
    for folder, extensions in EXTENSIONS.items():
        if ext.lower() in extensions:
            destination = os.path.join(os.path.expanduser("~/Downloads/trained_data"), folder)
            os.makedirs(destination, exist_ok=True)
            shutil.move(file_path, os.path.join(destination, os.path.basename(file_path)))
            print(f"Moved {file_path} → {destination}")
            print("\n")

            return
    print(f"Skipped: {file_path}")

directory = (os.path.expanduser("~/Downloads/trained_data"))
with os.scandir(directory) as files:
    for file in files:
        # print(file.path)
        _, ext = os.path.splitext(file.path)
        for folder, extensions in EXTENSIONS.items():
            if ext.lower() in extensions:
                destination = os.path.join(os.path.expanduser("~/Downloads/trained_data/"), folder)
                os.makedirs(destination, exist_ok=True)
                shutil.move(file.path, os.path.join(destination, os.path.basename(file.path)))
                print(Fore.WHITE + Back.GREEN + "[MOVED]" + Style.RESET_ALL +  " <==> " + f"{file.path} → {destination}")
                print("\n")
                break

        if file.is_file():
            # print(file.is_file())
            print(Fore.WHITE + Back.RED + "[SKIPPED]" + Style.RESET_ALL + " <==> " + f"'{file.path}'")
            # print("\n")
        else:
            file.is_dir()
            pass

colorama.deinit()
#
# Deduplicate files
def is_duplicate(file_path, directory):
    file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    for root, _, files in os.walk(directory):
        for file in files:
            other_file_path = os.path.join(root, file)
            if file_path != other_file_path:
                other_hash = hashlib.md5(open(other_file_path, 'rb').read()).hexdigest()
                if file_hash == other_hash:
                    return True
    return False
#
# # Monitor folder changes
# class Watcher(FileSystemEventHandler):
#     def on_created(self, event):
#         if event.is_directory:
#             return
#         file_path = event.src_path
#         if not is_duplicate(file_path, os.path.expanduser("~/Downloads")):
#             organize_file(file_path)
#         else:
#             os.remove(file_path)
#             print(f"Deleted duplicate: {file_path}")
#
# # Start watching
# def start_watching(folder="~/Downloads"):
#     folder = os.path.expanduser(folder)
#     event_handler = Watcher()
#     observer = Observer()
#     observer.schedule(event_handler, folder, recursive=True)
#     observer.start()
#     print(f"Watching {folder}...")
#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
#
# if __name__ == "__main__":
#     start_watching()
