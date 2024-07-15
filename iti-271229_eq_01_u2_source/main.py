import sys
from PyQt6.QtWidgets import QApplication
from grid import *

def main():
    """
    Crear instancia del Grid y desplegar ventana
    """
    app = QApplication(sys.argv)   

    #Se obtiene la pantalla de la aplicación
    screen = app.primaryScreen()    

    #Se obtiene el tamaño de la pantalla
    size = screen.size()

    #La aplicación se redimenziona de acuerdo al tamaño de la pantalla
    window = Grid(size.width(), size.height())
    sys.exit(app.exec())

#Ejecutar programa
if __name__ == '__main__':
    main()