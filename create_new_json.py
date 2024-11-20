import json
from deep_translator import GoogleTranslator

def load_json(file_path):
    """Carga un archivo JSON y devuelve su contenido."""
    print(f"Loading JSON file from: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print(f"Successfully loaded JSON file with {len(data)} items.")
        return data

def save_json(data, file_path):
    """Guarda un diccionario en un archivo JSON."""
    print(f"Saving JSON file to: {file_path} with {len(data)} items.")
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Successfully saved JSON file to: {file_path}")

def process_data(data):
    """Procesa los datos para extraer Sentence, Author, y traducir las temáticas."""
    print("Processing data to extract and translate...")
    processed_data = []
    for idx, item in enumerate(data):
        # Extraer 'Sentence' y 'Author'
        processed_item = {
            'Sentence': item.get('Sentence', ''),
            'Author': item.get('Author', '')
        }
        
        # Traducir las temáticas y agregarlas
        for i in range(1, 4):
            thematic_key = f'Temática {i}'
            translated_key = f'thematic {i}'
            if thematic_key in item:
                thematic_value = item[thematic_key]
                if thematic_value:
                    translated = GoogleTranslator(source='es', target='en').translate(thematic_value)
                    processed_item[translated_key] = translated
                    print(f"Item {idx}: Translated '{thematic_key}' to '{translated_key}' - {translated}")
                else:
                    processed_item[translated_key] = ''
                    print(f"Item {idx}: '{thematic_key}' is empty, set '{translated_key}' to empty.")
            else:
                processed_item[translated_key] = ''
        
        processed_data.append(processed_item)
        
        # Eliminar 'Sentence' y 'Author' del original
        item.pop('Sentence', None)
        item.pop('Author', None)
        
    print("Processing complete.")
    return processed_data

def main():
    # Cargar el archivo original
    original_file = 'Oraciones.json'
    print("Starting main process...")
    data = load_json(original_file)
    
    # Procesar datos para extraer 'Sentence', 'Author' y traducir temáticas
    processed_data = process_data(data)
    
    # Guardar los datos procesados en un nuevo archivo JSON
    save_json(processed_data, 'Sentences.json')
    
    # Guardar el archivo original con 'Sentence' y 'Author' eliminados
    save_json(data, original_file)
    print("Main process completed.")

if __name__ == "__main__":
    main()
