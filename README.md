# Control-selector-de-tomates-Raspberry-Pi5
Control Selector de Tomates - Raspberry Pi 5
Sistema de visión artificial y control automatizado para la selección y clasificación de tomates utilizando Raspberry Pi 5.

🚀 Características
Detección en tiempo real con modelo YOLOv11 entrenado para tomates

Control preciso de servomotores para mecanismos de selección

Arquitectura modular separando detección y control

📁 Estructura del Proyecto
detector.py
Implementa el modelo YOLOv11 para detección de tomates

Procesa imágenes/video en tiempo real

Proporciona coordenadas y confianza de las detecciones

controlador.py
Recibe datos de detección del detector.py

Implementa lógica de control para servomotores

Ejecuta acciones de selección basadas en posición y características de los tomates

🔧 Aplicaciones
Automatización agrícola

Sistemas de clasificación de frutas

Proyectos de robótica con visión artificial
