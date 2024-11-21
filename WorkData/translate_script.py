from googletrans import Translator

def traducir_texto(texto):
    # Crear una instancia del traductor
    traductor = Translator()

    # Detectar el idioma del texto
    deteccion = traductor.detect(texto)
    idioma_origen = deteccion.lang

    # Determinar el idioma al que se va a traducir
    if idioma_origen == 'es':
        idioma_destino = 'en'
    elif idioma_origen == 'en':
        idioma_destino = 'es'
    else:
        return "Idioma no soportado. Solo se soportan textos en inglés o español."

    # Traducir el texto
    traduccion = traductor.translate(texto, src=idioma_origen, dest=idioma_destino)
    return traduccion.text

# Ejemplo de uso
if __name__ == "__main__":
    # Simulando que el texto proviene de otro script
    texto = "Hola, ¿cómo estás?"
    texto_traducido = traducir_texto(texto)
    print("Texto original:", texto)
    print("Texto traducido:", texto_traducido)

    # Otro ejemplo con inglés
    texto = "Hello, how are you?"
    texto_traducido = traducir_texto(texto)
    print("Texto original:", texto)
    print("Texto traducido:", texto_traducido)
