import os

def convertir_valores_a_float(directorio):
    # Obtener la lista de archivos en el directorio
    archivos_txt = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.txt')]

    # Recorrer cada archivo .txt
    for archivo in archivos_txt:
        ruta_archivo = os.path.join(directorio, archivo)
        print(f"Convirtiendo valores en {ruta_archivo}")

        # Leer el contenido del archivo
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()

        # Abrir el archivo para escritura
        with open(ruta_archivo, 'w') as f:
            for linea in lineas:
                # Dividir la línea en valores
                valores = linea.strip().split(',')
                
                # Convertir valores a float y volver a unirlos
                valores_float = [str(float(valor.strip())) for valor in valores]
                nueva_linea = ' '.join(valores_float) + '\n'
                
                # Escribir la línea convertida de vuelta al archivo
                f.write(nueva_linea)

    print("¡Conversión completada!")

# Ejemplo de uso
directorio_a_convertir = 'dataset/labels/train'
convertir_valores_a_float(directorio_a_convertir)

