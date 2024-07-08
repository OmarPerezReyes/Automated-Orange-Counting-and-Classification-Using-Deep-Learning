import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSlot
from window import Window

class Grid(QWidget):
    """
    Clase Grid
    Crea la interfaz (botones, dialogos) para el programa
    """
    def __init__(self):
        """
        Constructor
        Inicializa la clase (objeto)
        """
        super().__init__()        
        self.window = Window()        
        self.initUI()
    
    def initUI(self):
        """
        Inicializa los elementos a utilizar de la ventana
        """        
        # Crear instancias de Grid y Window
        grid = QGridLayout()        

        # Botón para abrir imagenes o videos
        openFileBtn = QPushButton('Seleccionar archivo')
        #openFileBtn.clicked.connect(lambda: self.window.playMedia(self.open_dialog()))
        openFileBtn.clicked.connect(self.open_dialog)
        
        #Botón para abrir la cámara
        openCameraBtn = QPushButton('Abrir cámara')
        openCameraBtn.clicked.connect(self.openCamera)
        
        #Layout horizontal
        layout = QHBoxLayout()

        # Añadir widgets al layoout horizontal
        layout.addWidget(openFileBtn)
        layout.addWidget(openCameraBtn)        
        
        #Añadir layout y ventana al grid
        grid.addLayout(layout, 0, 0)
        grid.addWidget(self.window, 1, 0)

        self.isCameraStarted = False

        # Anexar grid al layout y mostrar la ventana
        self.setLayout(grid)
        self.center()
        self.setWindowTitle('Orange counter')
        self.showMaximized()  

    def openCamera(self):
        """
        Iniciar cámara
        """
        if not self.isCameraStarted:            
            self.window.startCamera()
            self.isCameraStarted = True

    def closeCamera(self):
        """
        Detener cámara
        """
        if self.isCameraStarted:
            self.window.stopCamera()
            self.isCameraStarted = False

    @pyqtSlot()    
    def open_dialog(self):
        """
        Abrir el contenido multimedia
        Devuelve el path (URL) del archivo selecciondo
        """

        #Cerrar la cámara en caso de estar abierta
        self.closeCamera()

        #Ejecutar FileDialog para seleccionar archivo
        fname = QFileDialog.getOpenFileName(
            self,
            "Seleccionar video o imágen",
            "",
            "Imágenes y videos (*.mp4 *.avi *.mov *.jpg *.jpeg *.png *.bmp)",
        )

        if fname:
            self.window.playMedia(fname[0])

        #Devuelve el path (string) del archivo seleccionado
        #return fname[0]            

    def center(self):
        """
        Centrar ventana
        """
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())