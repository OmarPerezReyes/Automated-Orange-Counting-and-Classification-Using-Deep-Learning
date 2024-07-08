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

        #Eliminar al finalizar el test
        with open('coco.names','rt') as f:
            class_name = f.read().rstrip('\n').split('\n')    

        class_color = []
        for i in range(len(class_name)):
            class_color.append((randint(0,255),randint(0,255),randint(0,255)))

        modelPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightPath = 'frozen_inference_graph.pb'

        net = cv2.dnn_DetectionModel(weightPath, modelPath)
        net.setInputSize(320,320)                
        net.setInputScale(1.0/ 127.5)        
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)
        #Eliminar end        

        while self.isRunning:
            # Obtener resultado y frame de la captura
            result, frame = self.openMedia(capture)

            # Si no hay resultado de captura, intentar de nuevo
            if not result:             
                continue            

            #Eliminar al finalizar el test            
            classIds, confs, bbox = net.detect(frame, confThreshold=0.5) 
            if len(classIds) != 0:        
                for classId,confidence,box in zip(classIds.flatten(), confs.flatten(), bbox):     
                    print(classId)
                    if classId != 55:
                        break
                    cv2.rectangle(frame, box, color=class_color[classId-1], thickness=2)
                    cv2.putText(frame, class_name[classId-1].upper(),(box[0],box[1]-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,class_color[classId-1],2)                    
            #Eliminar

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