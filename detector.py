from ultralytics import YOLO
import time

# Cargar modelo YOLO
model = YOLO("best.pt")

# Archivo para comunicar el resultado
archivo_resultado = "/home/ra/yolo/deteccion.txt"

# Bucle continuo de detección
while True:
    results = model.predict(source=0, show=False, stream=True)  # cámara
    for r in results:
        # Obtener los nombres de las clases detectadas
        nombres_detectados = [model.names[int(c)] for c in r.boxes.cls]

        # Depuración: Imprimir las clases detectadas
        print("Clases detectadas:", nombres_detectados)

        # Solo estamos buscando "maduro" o "inmaduro"
        if "maduro" in nombres_detectados:
            with open(archivo_resultado, "w") as f:
                f.write("maduro")  # Guardar como "maduro"
        elif "inmaduro" in nombres_detectados:
            with open(archivo_resultado, "w") as f:
                f.write("inmaduro")  # Guardar como "inmaduro"
        else:
            with open(archivo_resultado, "w") as f:
                f.write("no_tomato")  # Si no se detecta tomate

        # Depuración: Imprimir lo que se escribió en el archivo
        print(f"Escrito en {archivo_resultado}: {nombres_detectados}")

        time.sleep(0.5)  # Para no sobrecargar la CPU
