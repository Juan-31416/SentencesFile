from googletrans import Translator

def translate_text(text, text_type='text'):
    try:
        translator = Translator()

        # Skip translation for empty strings
        if not text or text.strip() == '':
            return text

        # Detect the text language
        detection = translator.detect(text)
        source_language = detection.lang

        # Determine target language
        if source_language == 'es':
            target_language = 'en'
        elif source_language == 'en':
            target_language = 'es'
        else:
            return text  # Return original text if language not supported

        # Always translate the actual content
        translation = translator.translate(text, src=source_language, dest=target_language)
        return translation.text if translation and translation.text else text
        
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text on error

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
