import json
import os
from Languages.language_detector import detect_language  # This is the language detector function
from WorkData.translate_script import translate_text # This is the translation function

def add_data_to_file(data):
    # Extract information from the input dictionary
    text = data.get('text', '').strip()
    author = data.get('author', '').strip()
    theme = data.get('theme', '')  # Single theme

    if not text or not author or not theme:
        raise ValueError("Missing required fields")

    # Determine if the text is in Spanish or English
    language = detect_language(text)
    if not language:
        print("Language not detected, defaulting to English")
        language = "english"  # Default fallback
    
    try:
        # Translate text and author
        translated_text = translate_text(text, text_type='text')
        translated_author = translate_text(author, text_type='author')

        # Handle theme translation based on the source language
        if language == "spanish":
            # If original text is Spanish, theme is in Spanish and needs translation to English
            translated_theme = translate_text(theme, text_type='theme')
            spanish_entry = {
                "Oración": text,
                "Autor": author,
                "Temática": theme  # Original Spanish theme
            }
            english_entry = {
                "Sentence": translated_text,
                "Author": translated_author,
                "Theme": translated_theme  # Translated to English
            }
        else:
            # If original text is English, theme is in English and needs translation to Spanish
            translated_theme = translate_text(theme, text_type='theme')
            english_entry = {
                "Sentence": text,
                "Author": author,
                "Theme": theme  # Original English theme
            }
            spanish_entry = {
                "Oración": translated_text,
                "Autor": translated_author,
                "Temática": translated_theme  # Translated to Spanish
            }

        # Create Sentences directory if it doesn't exist
        os.makedirs('Sentences', exist_ok=True)

        # Save to respective files
        save_to_json(spanish_entry, 'Sentences/Oraciones.json')
        save_to_json(english_entry, 'Sentences/Sentences.json')
        
    except Exception as e:
        print(f"Error in add_data_to_file: {e}")
        raise

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
