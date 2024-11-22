import os
import yaml

def load_all_languages(languages_path):
    """Loads all language files from the specified directory"""
    languages = {}
    for filename in os.listdir(languages_path):
        if filename.endswith('.yaml'):
            with open(os.path.join(languages_path, filename), 'r', encoding='utf-8') as file:
                language_name = os.path.splitext(filename)[0]
                languages[language_name] = yaml.safe_load(file)
    return languages

