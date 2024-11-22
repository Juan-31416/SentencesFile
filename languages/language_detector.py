from langdetect import detect

def detect_language(text):
    try:
        language_map = {
            'es': 'spanish',
            'en': 'english'
        }
        # Devuelve 'english' por defecto si no es 'es' o 'en'.
        return language_map.get(detect(text), 'english')
    except Exception as e:
        print(f"Language detection error: {e}")
        return "english"

# Ejemplos de uso
texts = [
    "Este es un ejemplo de texto en español.",
    "This is an example of text in English.",
    "Ceci est un exemple de texte en français."
]

for text in texts:
    result = detect_language(text)
    print(result)

