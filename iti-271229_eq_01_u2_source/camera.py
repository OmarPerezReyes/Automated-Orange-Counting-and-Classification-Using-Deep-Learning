import os
import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QApplication, QWidget, QGridLayout, QPushButton, QFileDialog, QLabel
from PyQt6.QtGui import QImage, QPixmap

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
        cv2.destroyAllWindows()

    def stop(self):
        """
        Detener cámara (hilo)
        """
        self.isRunning = False
        
    def resume(self):
        self.isRunning = True    

    def updateSize(self, w, h):
        """
        Actualizar las dimensiones de la cámara
        Ajustar cámara al tamaño de la ventana
        """
        self.width = w
        self.height = h
