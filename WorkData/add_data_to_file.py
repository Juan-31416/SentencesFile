import json
import os
from typing import Dict
import logging
from Languages.language_detector import detect_language  # This is the language detector function
from WorkData.translate_script import translate_text  # This is the translation function

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

def add_data_to_file(data: Dict[str, str], gui_language: str) -> None:
    """
    Main function to add data to a file after processing.
    
    :param data: Dictionary containing text, author, and theme.
    :param gui_language: Current language of the GUI interface.
    """
    try:
        # Validate the input data and extract fields
        text, author, theme = validate_and_extract_data(data)
        
        # Determine the language of the provided text
        text_language = determine_language(text)
        
        # Create translated entries for both Spanish and English versions
        translated_entries = create_translated_entries(text, author, theme, text_language, gui_language)

        # Ensure Sentences directory exists
        os.makedirs('Sentences', exist_ok=True)

        # Save translated entries to respective JSON files
        save_to_json(translated_entries['spanish'], 'Sentences/Oraciones.json')
        save_to_json(translated_entries['english'], 'Sentences/Sentences.json')

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in add_data_to_file: {e}")
        raise

def validate_and_extract_data(data: Dict[str, str]) -> tuple:
    """
    Validates input data and extracts relevant fields.
    
    :param data: Dictionary containing text, author, and theme.
    :return: Tuple containing text, author, and theme.
    """
    # Extract and trim whitespace from text, author, and theme
    text = data.get('text', '').strip()
    author = data.get('author', '').strip()
    theme = data.get('theme', '').strip()

    # Check if any of the required fields are missing
    if not text or not author or not theme:
        raise ValueError("Missing required fields: 'text', 'author', and 'theme' must all be provided.")

    return text, author, theme

def determine_language(text: str) -> str:
    """
    Determines the language of the given text.
    
    :param text: Text to determine language for.
    :return: Detected language, defaults to 'english' if not detected.
    """
    # Use the language detector function to determine the language of the text
    language = detect_language(text)
    
    # If the language could not be detected, log a warning and default to English
    if not language:
        logging.warning("Language not detected, defaulting to English")
        language = "english"  # Default fallback

    return language

def create_translated_entries(text: str, author: str, theme: str, text_language: str, gui_language: str) -> Dict[str, Dict[str, str]]:
    """
    Creates translated entries for both Spanish and English.
    
    :param text: Original text.
    :param author: Original author.
    :param theme: Original theme.
    :param text_language: Detected language of the text.
    :param gui_language: Current language of the GUI interface.
    :return: Dictionary containing Spanish and English entries.
    """
    # Translate text and author
    translated_text = translate_text(text)
    translated_author = translate_text(author)
    
    # Handle theme translation based on GUI language
    if gui_language == "spanish":
        spanish_theme = theme
        english_theme = translate_text(theme, source_lang='es', target_lang='en')
    else:
        english_theme = theme
        spanish_theme = translate_text(theme, source_lang='en', target_lang='es')

    # Create entries based on the detected text language
    if text_language == "spanish":
        spanish_entry = {
            "Oración": text,
            "Autor": author,
            "Temática": spanish_theme
        }
        english_entry = {
            "Sentence": translated_text,
            "Author": translated_author,
            "Theme": english_theme
        }
    else:
        english_entry = {
            "Sentence": text,
            "Author": author,
            "Theme": english_theme
        }
        spanish_entry = {
            "Oración": translated_text,
            "Autor": translated_author,
            "Temática": spanish_theme
        }

    return {"spanish": spanish_entry, "english": english_entry}

def save_to_json(entry: Dict[str, str], filename: str) -> None:
    """
    Saves a dictionary entry to a JSON file.
    
    :param entry: Entry to be saved.
    :param filename: Path to the file where data should be saved.
    """
    try:
        # If the file does not exist, create a new list with the entry
        if not os.path.exists(filename):
            data = [entry]
        else:
            # If the file exists, read its content
            with open(filename, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    # Ensure the loaded data is a list
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    # If JSON decoding fails, start with an empty list
                    data = []

                # Append the new entry to the list
                data.append(entry)

        # Write the updated list back to the file
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    except IOError as e:
        logging.error(f"File error when saving to {filename}: {e}")
        raise

# Example usage:
if __name__ == "__main__":
    # Example data to be processed and saved
    submit_data = {
        'text': 'Este es un ejemplo de oración.',
        'author': 'Autor Ejemplo',
        'theme': 'Tema Ejemplo'
    }

    # Add the example data to the file
    add_data_to_file(submit_data, 'spanish')
