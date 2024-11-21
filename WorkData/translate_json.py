import json
from deep_translator import GoogleTranslator

# Inicializar el traductor
def leer_json(nombre_archivo):
    print(f"Leyendo el archivo JSON: {nombre_archivo}")
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    print(f"Datos leídos: {datos}")
    return datos

def traducir_datos(datos, idioma_destino):
    print(f"Traduciendo datos al idioma: {idioma_destino}")
    datos_traducidos = []
    for entrada in datos:
        print(f"Traduciendo entrada: {entrada}")
        oracion_traducida = GoogleTranslator(source='auto', target=idioma_destino).translate(entrada['Oración'])
        autor_traducido = GoogleTranslator(source='auto', target=idioma_destino).translate(entrada['Autor'])
        
        tematica_traducida = GoogleTranslator(source='auto', target=idioma_destino).translate(entrada.get('Temática', '')) if entrada.get('Temática') else ""
        
        nueva_entrada = {
            'Oración': oracion_traducida,
            'Autor': autor_traducido,
            'Temática': tematica_traducida
        }
        print(f"Nueva entrada traducida: {nueva_entrada}")
        datos_traducidos.append(nueva_entrada)
    return datos_traducidos

def guardar_json(datos, idioma_destino):
    nombre_archivo = "Oraciones" if idioma_destino == 'es' else "Sentences"
    print(f"Guardando los datos traducidos en el archivo: {nombre_archivo}.json")
    with open(f"{nombre_archivo}.json", 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)
    print(f"Datos guardados exitosamente en {nombre_archivo}.json")

def main():
    # Nombre del archivo de entrada
    archivo_entrada = 'oraciones.json'
    # Idioma al que se desea traducir (ejemplo: 'en' para inglés, 'fr' para francés, etc.)
    idioma_destino = input("Ingrese el código del idioma al que desea traducir (ejemplo: 'en' para inglés): ")
    
    # Leer el archivo JSON
    datos = leer_json(archivo_entrada)
    
    # Traducir los datos
    datos_traducidos = traducir_datos(datos, idioma_destino)
    
    # Guardar los datos traducidos en un nuevo archivo JSON
    guardar_json(datos_traducidos, idioma_destino)
    
    print(f"Archivo traducido guardado como '{'Oraciones' if idioma_destino == 'es' else 'Sentences'}.json'")

if __name__ == "__main__":
    main()
