import json
import os
from Languages.language_detector import detect_language  # This is the language detector function
from WorkData.translate_script import translate_text # This is the translation function

def add_data_to_file(data):
    # Extract information from the input dictionary
    text = data.get('text', '').strip()
    author = data.get('author', '').strip()
    themes = data.get('theme', '')

    # Determine if the text is in Spanish or English
    language = detect_language(text)  # "spanish" or "english" expected
    
    # Translate text, author, and themes
    translated_text = translate_text(text)
    translated_author = translate_text(author)
    translated_theme = translate_text(themes) if themes else ""

    # Prepare Spanish and English entries
    spanish_entry = {}
    english_entry = {}

    if language == "spanish":
        # Spanish text is original
        spanish_entry = {
            "Oración": text,
            "Autor": author,
            "Temática": themes
        }
        english_entry = {
            "Sentence": translated_text,
            "Author": translated_author,
            "Theme": translated_theme
        }
    else:
        # English text is original
        english_entry = {
            "Sentence": text,
            "Author": author,
            "Theme": themes
        }
        spanish_entry = {
            "Oración": translated_text,
            "Autor": translated_author,
            "Temática": translated_theme
        }

    # Remove empty values
    spanish_entry = {k: v for k, v in spanish_entry.items() if v}
    english_entry = {k: v for k, v in english_entry.items() if v}

    # Save to respective files
    save_to_json(spanish_entry, 'Sentences/Oraciones.json') # Hardcoded path for this project
    save_to_json(english_entry, 'Sentences/Sentences.json') # Hardcoded path for this project

def save_to_json(entry, filename):
    if not os.path.exists(filename):
        data = [entry]
    else:
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
            
            data.append(entry)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Example usage:
submit_data = {
    'text': 'Este es un ejemplo de oración.',
    'author': 'Autor Ejemplo',
    'themes': ['Tema 1', 'Tema 2', 'Tema 3'],
    'output_format': 'json',
    'file_path': 'output.json'
}

# add_data_to_json(submit_data)  # Uncomment to run
