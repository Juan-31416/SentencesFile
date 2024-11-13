from langdetect import detect

def detect_language(text):
    try:
        language = detect(text)
        if language == 'es':
            return "spanish"
        elif language == 'en':
            return "english"
        else:
            return "unsupported language"
    except Exception as e:
        return f"Error detecting language: {e}"

# Example usage with text returned by another script
text = "Este es un ejemplo de texto en español."
result = detect_language(text)
print(result)

# Another example with text in English
text = "This is an example of text in English."
result = detect_language(text)
print(result)
