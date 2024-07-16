# Aplicación PyQt6 para el Conteo en Tiempo Real: Un Caso de Estudio con Detección de Naranjas

Este repositorio contiene el código fuente para la aplicación PyQt6 desarrollada para el artículo titulado "Aplicación PyQt6 para el Conteo en Tiempo Real: Un Caso de Estudio con Detección de Naranjas". Este artículo será presentado en el Congreso Nacional de Ciencias de la Computación 2024.

## Descripción

La aplicación está diseñada para detectar y contar naranjas en imágenes y videos en tiempo real utilizando un modelo pre-entrenado de TensorFlow y PyQt6 para la interfaz gráfica de usuario (GUI). El modelo de detección de objetos es SSD MobileNet V3, que se ha entrenado con el conjunto de datos COCO.

## Estructura del Repositorio

- `camera.py`: Código relacionado con la captura de video en tiempo real desde la cámara.
- `coco.names`: Archivo con los nombres de las clases del conjunto de datos COCO.
- `frozen_inference_graph.pb`: Modelo de TensorFlow pre-entrenado.
- `ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt`: Archivo de configuración del modelo.
- `grid.py`: Código para gestionar la disposición de widgets en la GUI.
- `main.py`: Archivo principal para ejecutar la aplicación.
- `media/`: Carpeta que contiene imágenes y videos de prueba.
- `player.py`: Código relacionado con la reproducción de medios (imágenes y videos).
- `window.py`: Código para la creación y gestión de la ventana principal de la GUI.

## Requisitos

- Python 3.x
- PyQt6
- TensorFlow
- OpenCV

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/OmarPerezReyes/Automated-Orange-Counting-and-Classification-Using-Deep-Learning.git
    cd Automated-Orange-Counting-and-Classification-Using-Deep-Learning
    ```

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

## Ejecución de la Aplicación

Para ejecutar la aplicación, simplemente escribe el siguiente comando en la terminal:

```bash
python3 main.py
