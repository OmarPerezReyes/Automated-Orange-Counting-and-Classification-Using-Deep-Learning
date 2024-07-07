from ultralytics import YOLO

# Descargar y cargar un modelo preentrenado de YOLOv5
model = YOLO('yolov8s.pt')  # Puedes usar otros modelos como yolov5m.pt, yolov5l.pt, etc.

# Entrenar el modelo con tu propio conjunto de datos
# Asegúrate de que tu conjunto de datos esté en formato YOLO (anotaciones en .txt y las imágenes correspondientes)
model.train(data='dataset/data.yaml', epochs=100)

# Evaluar el modelo
results = model.val()

# Realizar predicciones
#img = 'dataset/images/val/arbol_naranjas201.png'
#results = model(img)

# Mostrar resultados
#results.show()
