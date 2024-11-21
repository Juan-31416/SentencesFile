import os
import yaml

def load_all_languages():
    """Loads all language files from the languages directory"""
    languages = {}
    languages_dir = "languages"
    try:
        for filename in os.listdir(languages_dir):
            if filename.endswith('.yaml'):
                language_name = filename[:-5].lower()  # Remove .yaml and convert to lowercase
                file_path = os.path.join(languages_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    languages[language_name] = yaml.safe_load(file)
        return languages
    except Exception as e:
        print(f"Error loading language files: {e}")
        # Provide a basic fallback
        return {
            "Spanish": {
                "window_title": "Interfaz de Entrada de Texto",
                "insert_text": "Insertar texto aquí",
                "author": "Autor",
                "output": "Salida",
                "submit": "Enviar",
                "documentation": "Documentación",
                "about": "Acerca de",
                "themes": [
                    "Cultura",
                    "Desarrollo personal",
                    "Economía",
                    "Emprendimiento",
                    "Finanzas",
                    "Filosofía",
                    "Historia",
                    "Liberalismo",
                    "Mentalidad",
                    "Moral",
                    "Motivación",
                    "Negocios",
                    "Política",
                    "Psicología",
                    "Relaciones",
                ],
                "path_menu": "Ruta",
                "language_menu": "Idioma",
                "help_menu": "Ayuda",
                "open_directory": "Abrir Directorio",
                "language_english": "Inglés",
                "language_spanish": "Español"
            }
        } 