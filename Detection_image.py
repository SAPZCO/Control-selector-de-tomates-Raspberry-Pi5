from ultralytics import YOLO
import cv2

# Cargamos el modelo YOLO
model = YOLO("best.pt")

# Cargamos el video (en este caso, cámara web)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Realizamos la inferencia
    results = model(frame)

    # Dibujamos los resultados en el frame
    annotated_frame = results[0].plot()

    # Obtenemos las etiquetas detectadas
    names = model.names  # Diccionario de clases: {0: 'maduro', 1: 'inmaduro', ...}

    for box in results[0].boxes:
        cls_id = int(box.cls[0])  # ID de clase detectada
        label = names[cls_id]     # Nombre de clase
        print(label)              # Imprime solo “maduro” o “inmaduro”

    # Mostramos el frame con las detecciones
    cv2.imshow("YOLO Inference", annotated_frame)

    # Presionar ESC para salir
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
