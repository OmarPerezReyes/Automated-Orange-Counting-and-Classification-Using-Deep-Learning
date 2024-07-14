import os
import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QApplication, QWidget, QGridLayout, QPushButton, QFileDialog, QLabel
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor, QFont

from math import sqrt

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
                            if hypotenuse < max(w1 // 2, w2 //2) or hypotenuse < max(h1 // 2, h2 // 2):
                                keep = False
                                break
                        if keep:
                            oranges.append(boxes[i])

                # Dibujar las detecciones
                for orange in oranges:                    
                    cv2.rectangle(frame, orange, color=(36, 255, 12), thickness=2)
                    counter += 1                  
            
            # Convertir el frame actual de formato BGR A RGB
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Tamaños de la imagen RGB
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w        

            #Convertir captura a un formato de QT    
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)            
            pix = convertToQtFormat.scaledToHeight(self.height, Qt.TransformationMode.SmoothTransformation)

            #Dibujar contador
            image = self.setCounter(pix, counter).toImage()

            #Actualizar Pixmap
            self.changePixmap.emit(image)     
        # Liberar captura
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
