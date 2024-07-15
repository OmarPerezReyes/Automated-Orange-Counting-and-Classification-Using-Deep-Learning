import os
import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMutex
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor, QFont
import numpy as np

from math import sqrt

class Player(QThread):
    """
    Reproduce los archivos multimedia seleccionados por el usuario
    """
    changePixmap = pyqtSignal(QImage)

    def __init__(self, width, height):
        super().__init__()

        #Abrir y crear array de clases (COCO)
        with open('coco.names','rt') as f:
            self.class_name = f.read().rstrip('\n').split('\n')

        #Path al modelo
        config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        frozen_model = 'frozen_inference_graph.pb'

        #Establever modelo de detección
        self.model = cv2.dnn_DetectionModel(frozen_model, config_file)
        self.model.setInputSize(320, 320)
        self.model.setInputScale(1.0 / 127.5)        
        self.model.setInputMean((127.5, 127.5, 127.5))
        self.model.setInputSwapRB(True)

        #Confianza por defecto
        self.confidence = 0.5

        #URL del archivo multimedia a reproducir
        self.url = ''

        #Reproductor en ejecución
        self.isRunning = True

        #Tamaños de la cámara (label)
        self.width = width
        self.height = height

    def updateSize(self, w, h):
        """
        Actualizar las dimensiones del reproductor
        Ajustar contenido al tamaño de la ventana
        """
        self.width = w
        self.height = h

    def setUrl(self, url):
        """
        Definir URL (Path) del archivo a reproducir
        """
        self.url = url        

    def run(self):
        """
        Método por defecto para correr el hilo
        """        
        self.play()     

    def updateConfidence(self, confidence):
        """
        Actualiza la confiaza del modelo
        """
        self.confidence = confidence

    def play(self):
        """
        Reproducir multimedia
        """                
        if self.url == '':
            return        

        # Obtener captura de la url
        capture = ''

        #Abrir captura solo si hay una URL (Path) disponible
        if self.url != '':   

            #Determinar la extesnión
            file_name, extension = os.path.splitext(self.url) 

            if extension in ['.jpg', '.jpeg', '.png']:
                capture = cv2.imread(self.url)
            else:            
                capture = cv2.VideoCapture(self.url)        
            
        while self.isRunning:
            # Obtener resultado y frame_copy de la captura        
            result, frame = self.openMedia(capture)

            #Crear copia de la imagen para dibujar sobre                           
            frame_copy = frame.copy()

            # Si no hay resultado de captura, intentar de nuevo
            if not result:                
                continue            

            #Inicializar contador
            counter = 0

            #Detectar objetos en la captura
            classIds, confs, bbox = self.model.detect(frame_copy, confThreshold=self.confidence) 

            #Si se detecta algo, se verifica que sea una naranja
            if len(classIds) != 0:     
                
                #Lista de cajas detectadas
                boxes = []                

                #Recorrer todos los oobjetos detectados por la API
                for classId, box in zip(classIds.flatten(), bbox):                    
                    if classId != 55:
                        continue
                    #Agregar a la lista solo las naranjas detectadas
                    boxes.append(box)

                #Lista de naranjas detectadas
                oranges = []

                #Recorrer las naranjas para determinar que no se intersecten las detecciones (recuadros)
                for i in range(len(boxes)):
                    #Agregar la primera naranja detectada
                    if not oranges:
                        oranges.append(boxes[i])

                    #Determinar si las demás naranjas detectadas de intersectan con las naranjas guardadas
                    else:
                        keep = True

                        #Recorrer las detecciones y compararlas con las ya guardadas
                        for orange in oranges:
                            #Valores de la detección no guardada
                            x1, y1, w1, h1 = boxes[i]

                            # Valores de la naranja/detección guardada
                            x2, y2, w2, h2 = orange

                            #Distancia entre los rectangulos (hipotenusa)
                            #h = sqrt(a^2 + b^2)
                            hypotenuse = sqrt((x1 - x2)**2 + (y1 - y2)**2)

                            #Ignorar caja detectada no guardada si está muy cerca (mitad del ancho y mitad del largo)
                            #de alguna caja ya guaradada
                            if hypotenuse < max(w1 // 2, w2 //2) and hypotenuse < max(h1 // 2, h2 // 2):
                                keep = False
                                break
                        if keep:
                            oranges.append(boxes[i])

                # Dibujar las detecciones
                for orange in oranges:                    
                    counter += 1
                    cv2.rectangle(frame_copy, orange, color=(36, 255, 12), thickness=2)
                    #x, y = orange[2:4]
                    #cv2.putText(frame_copy, str(counter), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, color=(0,0,255))

            #Convertir el frame_copy actual de formato BGR A RGB
            rgbImage = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)

            #Tamaños de la imagen RGB
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w

            #Convertir captura y redimenzionar a un formato de QT
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)                        

            #Escalar frame de imagen dependiendo de si la imagen es mayor a la resoluación de la pantalla actual
            if self.width <= frame.shape[0] or self.height <= frame.shape[1]:
                pix = convertToQtFormat.scaled(self.width, self.height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            else:
                pix = convertToQtFormat.scaledToHeight(self.height, Qt.TransformationMode.SmoothTransformation)            

            #Dibujar contador
            image = self.setCounter(pix, counter).toImage()

            #Actualizar Pixmap
            self.changePixmap.emit(image)

            cv2.destroyAllWindows()
        #Liberar captura
        if type(capture) == cv2.VideoCapture:
            capture.release()
        #cv2.destroyAllWindows()

    def setCounter(self, pix, counter):
        """
        Dibuja/imprime el contador en la imagen
        """
        # Crear un QPixmap
        pixmap = QPixmap.fromImage(pix)
        
        # Inicio QPainter
        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 0, 0))  # Color del texto en rojo
        
        # Configurar el tamaño del font
        font = QFont()
        font.setPointSize(25)
        painter.setFont(font)
        
        # Dibujar el contador en la esquina superior izquierda
        painter.drawText(50, 50, str(counter))
        
        # Fin QPainter
        painter.end()

        return pixmap

    def stop(self):
        """
        Detener reproductor
        """        
        self.isRunning = False               

    def resume(self):
        """
        Reanudar el reproductor
        """      
        self.isRunning = True

    def openMedia(self, capture):
        """
        Determinar el tipo de archivo
        """
        #Devolver falso en caso de que no haya una URL (Path)
        if self.url == '':            
            return False, capture
        
        if type(capture) == cv2.VideoCapture: #Video
            result, frame_copy = capture.read()
            return result, frame_copy
        else:            
            return True, capture #Imágenes