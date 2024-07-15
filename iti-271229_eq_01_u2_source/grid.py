import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QHBoxLayout, QPushButton, QSlider, QFileDialog
from PyQt6.QtCore import Qt, pyqtSlot
from window import Window

class Grid(QWidget):
    """
    Clase Grid
    Crea la interfaz (botones, dialogos) para el programa
    """
    def __init__(self, width, height):
        """
        Constructor
        Inicializa la clase (objeto)
        """
        super().__init__()                             
        self.window = Window(width - 10, height - 150)
        self.initUI()        
    
    def initUI(self):
        """
        Inicializa los elementos a utilizar de la ventana
        """        
        # Crear instancias de Grid y Window
        grid = QGridLayout()        

        # Botón para abrir imagenes o videos
        openFileBtn = QPushButton('Seleccionar archivo')        
        openFileBtn.clicked.connect(self.open_dialog)
        
        #Botón para abrir la cámara
        openCameraBtn = QPushButton('Abrir cámara')
        openCameraBtn.clicked.connect(self.openCamera)

        self.setConfidenceSlider = QSlider()     
        self.setConfidenceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.setConfidenceSlider.setRange(25, 75)
        self.setConfidenceSlider.setValue(50)
        self.setConfidenceSlider.setSingleStep(5)
        self.setConfidenceSlider.setPageStep(5)
        self.setConfidenceSlider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.setConfidenceSlider.valueChanged.connect(self.updateConfidence)

        self.conficenceLbl = QLabel('Confianza: 50')
        
        #Layout horizontal
        layout = QHBoxLayout()        

        # Añadir widgets al layoout horizontal
        layout.addWidget(openFileBtn)
        layout.addWidget(openCameraBtn)        
        
        #Añadir layout y ventana al grid
        grid.addLayout(layout, 0, 0)
        grid.addWidget(self.setConfidenceSlider, 1, 0)
        grid.addWidget(self.conficenceLbl, 2, 0)
        grid.addWidget(self.window, 3, 0)

        self.isCameraStarted = False

        # Anexar grid al layout y mostrar la ventana
        self.setLayout(grid)
        self.center()
        self.setWindowTitle('Orange counter')
        self.showMaximized()  

    def updateConfidence(self, value):
        """
        Actualiza la confianza del modelo.
        Actualiza el valor del label de confianza y actualiza a Window
        """
        confidence = value / 100
        self.conficenceLbl.setText(f'Confianza: {confidence}')
        self.window.updateConfidence(confidence)

    def openCamera(self):
        """
        Iniciar cámara
        """
        if not self.isCameraStarted:        
            self.setConfidenceSlider.setValue(50)    
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
            "Imágenes y videos (*.mp4 *.jpg *.jpeg *.png)",
        )

        #Si se selecciona una archivo se reproduce
        if fname:
            self.setConfidenceSlider.setValue(50)
            self.window.playMedia(fname[0])            

    def center(self):
        """
        Centrar ventana
        """
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())