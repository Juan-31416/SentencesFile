from py2exe import freeze
import os

# Function to collect all data files from a directory
def collect_data_files(directory):
    data_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        files = [os.path.join(dirpath, f) for f in filenames]
        data_files.append((dirpath, files))
    return data_files

# Collect all data files from the Languages, Help, and img directories
data_files = collect_data_files('Languages') + collect_data_files('Help') + collect_data_files('img')

# Add the langdetect messages.properties file
data_files.append(('nuevo_entorno/Lib/site-packages/langdetect/utils', ['nuevo_entorno/Lib/site-packages/langdetect/utils/messages.properties']))

freeze(
    console=[],
    windows=[{
        'script': 'GUI.py',  # Main script to convert to .exe
        'icon_resources': [(1, 'img/app_icon.ico')]  # Path to your icon file
    }],
    options={
        'packages': ['ttkbootstrap', 'yaml', 'langdetect'],  # Include any additional packages your script uses
        'includes': ['tkinter', 'ttkbootstrap.constants'],  # Include any modules that py2exe might miss
        'bundle_files': 1,  # Bundle everything into a single executable
        'compressed': True,  # Compress the library archive
    },
    data_files=data_files,  # Include data files
    zipfile=None,  # Bundle everything into the .exe
)