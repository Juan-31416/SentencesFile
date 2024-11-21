from googletrans import Translator

def translate_text(text, text_type='text'):
    # Create a translator instance
    translator = Translator()

    # Skip translation for empty strings
    if not text or text.strip() == '':
        return text

    # Detect the text language
    detection = translator.detect(text)
    source_language = detection.lang

    # Handle specific text types
    if text_type == 'author':
        # For author, translate between "Autor" and "Author"
        return "Author" if source_language == 'es' else "Autor"
    elif text_type == 'theme':
        # For theme, translate between "Temática" and "Theme"
        return "Theme" if source_language == 'es' else "Temática"

    # Determine the target language for regular text
    if source_language == 'es':
        target_language = 'en'
    elif source_language == 'en':
        target_language = 'es'
    else:
        return "Language not supported. Only English or Spanish texts are supported."

    # Translate the text
    translation = translator.translate(text, src=source_language, dest=target_language)
    return translation.text

# Usage example
if __name__ == "__main__":
    # Simulating text coming from another script
    text = "Hola, ¿cómo estás?"
    translated_text = translate_text(text)
    print("Original text:", text)
    print("Translated text:", translated_text)

    # Another example with English
    text = "Hello, how are you?"
    translated_text = translate_text(text)
    print("Original text:", text)
    print("Translated text:", translated_text)
