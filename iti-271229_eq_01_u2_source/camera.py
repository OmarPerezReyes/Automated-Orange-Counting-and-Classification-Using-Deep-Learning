import os
import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QApplication, QWidget, QGridLayout, QPushButton, QFileDialog, QLabel
from PyQt6.QtGui import QImage, QPixmap

from random import randint

class Camera(QThread):
    """
    Clase Camara
    Crea una instancia de la camara
    """
    changePixmap = pyqtSignal(QImage)

    def __init__(self, width, height):
        """
        Inicializar elementos de la clase
        """
        super().__init__()

        #Abrir y crear array de clases (COCO)
        with open('coco.names','rt') as f:
            self.class_name = f.read().rstrip('\n').split('\n')

        #Path al modelo
        model = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weight = 'frozen_inference_graph.pb'

        #Establever modelo de detección
        self.model = cv2.dnn_DetectionModel(weight, model)
        #self.model.setInputSize(320, 320)
        self.model.setInputSize(450, 450)
        self.model.setInputScale(1.0 / 127.5)        
        self.model.setInputMean((127.5, 127.5, 127.5))
        self.model.setInputSwapRB(True)

        #Cámara corriendo
        self.isRunning = True

        #Tamaños de la cámara (label)
        self.width = width
        self.height = height         

    def run(self):
        """
        Ejecutar cámara (hilo)
        """
        # Obtener captura de la cámara
        capture = cv2.VideoCapture(0, cv2.CAP_V4L2)        

        # Validar que se encontró una cámara, si no retornar
        if not capture.isOpened():
            return

        while self.isRunning:
            # Obtener resultado y frame de la captura
            result, frame = capture.read()

            # Si no hay resultado de captura, intentar de nuevo
            if not result:
                continue

            #Inicializar contador
            counter = 0                

            #Detectar objetos en la captura
            classIds, confs, bbox = self.model.detect(frame, confThreshold=0.25) 

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
            cv2.putText(frame, str(counter), (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255) , 2)
            
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
        capture.release()
        #cv2.destroyAllWindows()

    def stop(self):
        """
        Detener cámara (hilo)
        """
        self.isRunning = False   
        self.wait()      
        
    def resume(self):
        self.isRunning = True    

    def updateSize(self, w, h):
        """
        Actualizar las dimensiones de la cámara
        Ajustar cámara al tamaño de la ventana
        """
        self.width = w
        self.height = h
