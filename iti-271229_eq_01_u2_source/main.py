import sys
from PyQt6.QtWidgets import QApplication
from grid import *

def main():
    """
    Crear instancia del Grid y desplegar ventana
    """
    app = QApplication(sys.argv)    
    window = Grid()
    sys.exit(app.exec())

#Ejecutar programa
if __name__ == '__main__':
    main()