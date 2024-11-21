import os
import yaml

def load_all_languages():
    """Loads all language files from the languages directory"""
    languages = {}
    languages_dir = "languages"
    try:
        for filename in os.listdir(languages_dir):
            if filename.endswith('.yaml'):
                language_name = filename[:-5].lower()  # Remove .yaml and convert to lowercase
                file_path = os.path.join(languages_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    languages[language_name] = yaml.safe_load(file)
        return languages
    except Exception as e:
        print(f"Error loading language files: {e}")
        # Provide a basic fallback
        return {
            "english": {
                "window_title": "Text Input GUI",
                "insert_text": "Insert text here",
                "author": "Author",
                "output": "Output",
                "submit": "Submit",
                "documentation": "Documentation",
                "about": "About",
                "path_menu": "Path",
                "language_menu": "Language",
                "help_menu": "Help",
                "open_directory": "Open Directory"
            }
        } 