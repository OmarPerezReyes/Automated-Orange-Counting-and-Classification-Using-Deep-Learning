import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSize, QRect, pyqtSlot

from camera import *
from player import *

class Window(QMainWindow):
    """
    Clase Window
    Se encarga de dibujar los datos
    """
    def __init__(self):
        """
        Constructor
        Inicializa los elementos de la clase (objeto)
        """             
        super().__init__()        
        self.initUI()
        self.setStyleSheet("background-color: black;")
    
    def __del__(self):        
        """
        Destructor
        Detiene el hilo de la cámara activa y libera la memoria del objeto        
        """        
        self.stopCamera()
        del self.camera

    def initUI(self):
        """
        Inicializa los elementos de la interfaz
        """

        #Determinar si hay algo reproduciendose (Cámara/Reproductor)
        self.isMediaOpened = [False, False]

        # Obtener el ancho y la altura de la ventana
        self.width = self.width()
        self.height = self.height()

        # Crear un QLabel para mostrar la imagen
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width, self.height)   
        
        #Camara
        self.camera = Camera(self.width, self.height)
        self.camera.changePixmap.connect(self.setImage)

        #Reproductor
        self.player = Player(self.width, self.height)
        self.player.changePixmap.connect(self.setImage)

    def paintEvent(self, event):
        """
        Dibuja los elementos graficos        
        """
        qp = QPainter()        
                
        # Inicio QPainter
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            
        # Fin QPainter
        qp.end()

    @pyqtSlot(QImage)
    def setImage(self, image):
        """
        Actualizar imagen de la cámara
        """
        self.label.setPixmap(QPixmap.fromImage(image))

    def resizeEvent(self, event):
        """
        Actualiza los elementos de la ventana al redimensionar la pantalla
        """
        width = event.size().width()
        height = event.size().height()

        self.label.resize(width, height)

        # Actualizar el tamaño de la cámara
        self.updateCamera(width, height)

        self.update()

    def startCamera(self):
        """
        Iniciar cámara
        """
        #Cambiar estado a activo
        self.isMediaOpened[0] = True

        #Detener la reproducción de multimedia en caso de que la haya
        if self.isMediaOpened[1]:
            self.stopMedia()         

        #Iniciar cámara        
        self.camera.resume()
        self.camera.start()        

    def stopCamera(self):      
        self.isMediaOpened[0] = False
        self.camera.stop()

    def playMedia(self, url):    
        #Cambiar estado a activo
        self.isMediaOpened[1] = True

        #Detener la cámara en caso de que esté activa
        if self.isMediaOpened[0]:
            self.stopCamera()  

        #Iniciar reproductor                
        self.player.setUrl(url)
        self.player.resume()
        self.player.start()        

    def stopMedia(self):
        self.isMediaOpened[1] = False
        self.player.stop()     

    def updateCamera(self, width, height):
        """
        Actualiza los valores de la camara
        """
        self.camera.updateSize(width, height)        