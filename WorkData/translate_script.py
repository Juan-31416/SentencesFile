from googletrans import Translator
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Initialize the translator instance globally
translator = Translator()

# Default language settings
DEFAULT_SOURCE_LANG = 'es'
DEFAULT_TARGET_LANG = 'en'

def translate_text(text: str, source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> str:
    """
    Translate text between specified languages.

    :param text: The text to be translated.
    :param source_lang: The source language code (optional).
    :param target_lang: The target language code (optional).
    :return: Translated text or original text in case of an error.
    """
    try:
        # Skip translation for empty strings
        if not text.strip():
            return text

        # Detect the text language if not provided
        if not source_lang:
            detection = translator.detect(text)
            source_lang = detection.lang

        # Set default target language based on detected source language
        if not target_lang:
            if source_lang == DEFAULT_SOURCE_LANG:
                target_lang = DEFAULT_TARGET_LANG
            elif source_lang == DEFAULT_TARGET_LANG:
                target_lang = DEFAULT_SOURCE_LANG
            else:
                # Return original text if language not supported
                return text

        # Translate the text
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text if translation and translation.text else text

    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text  # Return original text on error

# Usage example
if __name__ == "__main__":
    # Simulating text coming from another script
    texts = ["Hola, ¿cómo estás?", "Hello, how are you?", "Bonjour, comment ça va?"]
    
    for text in texts:
        translated_text = translate_text(text)
        print(f"Original text: {text}")
        print(f"Translated text: {translated_text}\n")
