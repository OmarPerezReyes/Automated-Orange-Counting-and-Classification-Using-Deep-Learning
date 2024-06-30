import cv2
import os
import numpy as np

class FaceTrainer():
    """
    Entrena el modelo al ejecutar el programa
    """
    def __init__(self):
        self.dataset_path = "data/"

    def readImages(self):
        """
        Leer las imagenes del directorio seleccionado
        Devuelve las imagenes, labels (numpy_array) y dicionario de labels
        """
        images = []
        labels = []
        label_names = []        
        current_label = 0

        print('El tiempo de inicio de la aplicación puede variar dependiendo de la cantidad de datos del dataset (total de imagenes)')
        print('Entrenando modelo. Espere por favor...')
        
        #Recorrer todos los directorios del dataset
        for person in os.listdir(self.dataset_path):
            #Directorio (URL) de la persona
            person_path = os.path.join(self.dataset_path, person)

            #Verificar que la URL es un directorio
            if not os.path.isdir(person_path):
                continue
            
            #Asignar etiqueta númerica a los labels
            label_names.append(person)
            
            #Leer las imagenes en escala de grises
            for image in os.listdir(person_path):
                image_path = os.path.join(person_path, image)
                #image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                image = cv2.imread(image_path, 0)
                images.append(image)
                labels.append(current_label)
            
            #Incrementar el label actual
            current_label += 1
        

        #Crear modelo y entrenarlo
        model = cv2.face.EigenFaceRecognizer_create()
        model.train(images, np.array(labels))

        # Almacenando el modelo obtenido para usarlo como referencia
        model.write('user_models/teamModel.xml')

        print('Guardando modelo. Espere por favor...')