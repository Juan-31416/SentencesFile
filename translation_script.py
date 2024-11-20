import json
from googletrans import Translator

# Inicializar el traductor de Google
translator = Translator()

# Función para traducir el texto
def translate_text(text, src_language, dest_language):
    try:
        print(f"Traduciendo texto: '{text}' de {src_language} a {dest_language}")
        translated = translator.translate(text, src=src_language, dest=dest_language)
        print(f"Traducción exitosa: '{translated.text}'")
        return translated.text
    except Exception as e:
        print(f"Error al traducir el texto '{text}': {e}")
        return text

# Cargar el JSON desde un archivo
def load_json_file(filename):
    print(f"Cargando archivo JSON: '{filename}'")
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"Archivo JSON cargado exitosamente: {data}")
    return data

# Guardar el JSON en un archivo
def save_json_file(filename, data):
    print(f"Guardando archivo JSON: '{filename}'")
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Archivo JSON guardado exitosamente: '{filename}'")

# Procesar el JSON para completar las traducciones necesarias
def process_json(data):
    print("Iniciando el procesamiento del JSON para traducciones necesarias")
    for index, item in enumerate(data):
        print(f"Procesando elemento {index + 1}: {item}")
        # Traducir "Oración" al inglés si "Sentence" está vacío
        if item.get("Oración") and not item.get("Sentence"):
            print(f"'Sentence' vacío, traduciendo 'Oración' al inglés para el elemento {index + 1}")
            item["Sentence"] = translate_text(item["Oración"], 'es', 'en')

        # Traducir "Sentence" al español si "Oración" está vacío
        if item.get("Sentence") and not item.get("Oración"):
            print(f"'Oración' vacío, traduciendo 'Sentence' al español para el elemento {index + 1}")
            item["Oración"] = translate_text(item["Sentence"], 'en', 'es')

        # Traducir "Autor" al inglés y agregar el par "Author"
        if item.get("Autor"):
            print(f"Traduciendo 'Autor' al inglés para el elemento {index + 1}")
            item["Author"] = translate_text(item["Autor"], 'es', 'en')

    print("Procesamiento del JSON completado")
    return data

# Programa principal
def main():
    # Nombre del archivo JSON a procesar
    input_filename = "frases.json"
    output_filename = "frases_v2.json"

    # Cargar el archivo JSON
    data = load_json_file(input_filename)

    # Procesar las traducciones
    processed_data = process_json(data)

    # Guardar los datos procesados en un nuevo archivo JSON
    save_json_file(output_filename, processed_data)
    print(f"Archivo procesado y guardado como '{output_filename}'")

if __name__ == "__main__":
    main()
