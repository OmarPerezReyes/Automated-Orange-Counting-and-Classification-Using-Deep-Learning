import os
import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap

from random import randint

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
        self.play()             

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

            #Intentar abrir video
            capture = cv2.VideoCapture(self.url)            

            #Si no se puede abrir el video, entonces es una imágen
            if not capture.isOpened():            
                capture = cv2.imread(self.url)                    

        while self.isRunning:
            # Obtener resultado y frame de la captura
            result, frame = self.openMedia(capture)

            # Si no hay resultado de captura, intentar de nuevo
            if not result:             
                continue          

            #Inicializar contador
            counter = 0                  

            #Detectar objetos en la captura
            classIds, confs, bbox = self.model.detect(frame, confThreshold=0.5) 

            #Si se detecta algo, se verifica que sea una naranja
            if len(classIds) != 0:                

                #Recorrer objetos de acuerdo a su posición
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):                         
                    if classId != 55:
                        continue

                    #Aumentar contador
                    counter += 1

                    #Colocar cajas y textos del objeto (naranja)
                    cv2.rectangle(frame, box, color = (36, 255, 12), thickness = 2)
                    cv2.putText(frame, self.class_name[classId-1].upper() + ' #' + str(counter), (box[0], box[1] - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (36, 255, 12), 2)

            #Colocar contador en la esquina superior izquierda
            cv2.putText(frame, str(counter), (100, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255) , 1)

            # Convertir el frame actual de formato BGR A RGB
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Tamaños de la imagen RGB
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w            

            #Convertir captura a un formato de QT    
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
            p = convertToQtFormat.scaled(self.width, self.height, Qt.AspectRatioMode.IgnoreAspectRatio)

            #Actualizar Pixmap
            self.changePixmap.emit(p)
        # Liberar captura
        if type(capture) == cv2.VideoCapture:
            capture.release()
        #cv2.destroyAllWindows()

    def stop(self):
        """
        Detener reproductor
        """        
        self.isRunning = False        

    def resume(self):        
        self.isRunning = True

    def openMedia(self, capture):
        """
        Determinar el tipo de archivo
        """
        #Devolver falso en caso de que no haya una URL (Path)
        if self.url == '':
            return False, capture

        #Determinar el tipo de archivo
        if type(capture) == cv2.VideoCapture: #Video            
            result, frame = capture.read()
            return result, frame
        else:
            return True, capture #Imágenes