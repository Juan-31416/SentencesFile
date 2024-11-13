import json
import os
from language_detector import detect_language  # This is the language detector function
from translate_script import traducir_texto # This is the translation function

def add_data_to_json(data):
    # Extract information from the input dictionary
    text = data.get('text', '').strip()
    author = data.get('author', '').strip()
    themes = data.get('themes', [])
    output_format = data.get('output_format', 'json')
    file_path = data.get('file_path', '').strip()

    # If file path is empty, raise an error
    if not file_path:
        raise ValueError("File path is required.")

    # Determine if the text is in Spanish or English
    language = detect_language(text)  # "spanish" or "english" expected
    
    # Translate text to the other language
    translated_text = traducir_texto(text, 
                                   source_lang='es' if language == 'spanish' else 'en',
                                   target_lang='en' if language == 'spanish' else 'es')
    
    # Prepare data structure for JSON
    json_entry = {}
    if language == "spanish":
        json_entry["Oración"] = text
        json_entry["Sentence"] = translated_text
    else:
        json_entry["Sentence"] = text
        json_entry["Oración"] = translated_text
        
    json_entry["Autor"] = author if author else None

    # Add themes to the appropriate "Temática" keys, up to three themes
    for i, theme in enumerate(themes[:3], start=1):
        json_entry[f"Temática {i}"] = theme if theme else None

    # Remove keys with None values
    json_entry = {k: v for k, v in json_entry.items() if v is not None}

    # Check if file exists; create if it doesn't
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([json_entry], file, indent=4)
    else:
        # Append to the existing JSON file
        with open(file_path, 'r+') as file:
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("JSON file must contain an array of objects.")
            except json.JSONDecodeError:
                # File exists but is empty or invalid JSON; start a new array
                data = []
            
            data.append(json_entry)
            file.seek(0)
            json.dump(data, file, indent=4)

# Example usage:
submit_data = {
    'text': 'Este es un ejemplo de oración.',
    'author': 'Autor Ejemplo',
    'themes': ['Tema 1', 'Tema 2', 'Tema 3'],
    'output_format': 'json',
    'file_path': 'output.json'
}

# add_data_to_json(submit_data)  # Uncomment to run
