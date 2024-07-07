import cv2
import numpy as np
import os

# Función para leer etiquetas de varios archivos .txt y prepararlas para entrenamiento
def read_labels_from_txt_directory(txt_directory):
    all_data = []
    for filename in os.listdir(txt_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(txt_directory, filename)
            with open(file_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                
                # Extracción de etiquetas específicas para detección de naranjas
                x_center = float(parts[1])  # Coordenada x del centro de la naranja
                y_center = float(parts[2])  # Coordenada y del centro de la naranja
                width = float(parts[3])     # Ancho de la naranja
                height = float(parts[4])    # Alto de la naranja
                
                # Puedes agregar más características si es necesario
                
                # Aquí se puede construir el vector de características (X) y las etiquetas (Y)
                features = [x_center, y_center, width, height]
                label = 1  # Etiqueta positiva para la detección de naranjas
                
                all_data.append((features, label))
    
    return all_data

# Directorio que contiene todos los archivos .txt de etiquetas
txt_directory = 'dataset/labels/train'

# Leer etiquetas de todos los archivos .txt en el directorio
data = read_labels_from_txt_directory(txt_directory)

# Preparar datos para entrenamiento del SVM
X = np.array([entry[0] for entry in data], dtype=np.float32)
Y = np.array([entry[1] for entry in data], dtype=np.int32)

# Crear el clasificador SVM
svm = cv2.ml.SVM_create()
svm.setType(cv2.ml.SVM_C_SVC)
svm.setKernel(cv2.ml.SVM_LINEAR)  # Puedes ajustar el tipo de kernel según lo que funcione mejor para tus datos

# Entrenar el SVM
#svm.train(X, cv2.ml.ROW_SAMPLE, Y)
svm.train(np.array(X, dtype=np.float32), cv2.ml.ROW_SAMPLE, np.array(Y))

svm_file = cv2.FileStorage("svm_model.xml", cv2.FILE_STORAGE_WRITE)
svm.save('model.xml')
svm_file.release()

