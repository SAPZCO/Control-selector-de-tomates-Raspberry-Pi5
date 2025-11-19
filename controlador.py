import RPi.GPIO as GPIO
import time
import os

# -------------------- CONFIGURACIÓN INICIAL --------------------
GPIO.setmode(GPIO.BOARD)

# Pines de los motores
MOTOR2_PIN = 11
MOTOR3_PIN = 16
MOTOR4_PIN = 15

# Pines de los servos
servo_pins = [18]  # Solo un pin para el motor1 (puedes añadir más si es necesario)

# Configurar pines de los motores
GPIO.setup(MOTOR2_PIN, GPIO.OUT)
GPIO.setup(MOTOR3_PIN, GPIO.OUT)
GPIO.setup(MOTOR4_PIN, GPIO.OUT)

# Configurar pines de los servos
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)

# Crear PWM para los pines de los motores
motor2 = GPIO.PWM(MOTOR2_PIN, 50)  # 50 Hz
motor3 = GPIO.PWM(MOTOR3_PIN, 50)  # 50 Hz
motor4 = GPIO.PWM(MOTOR4_PIN, 50)  # 50 Hz

# Crear PWM para los servos (motor1)
pwms = [GPIO.PWM(pin, 50) for pin in servo_pins]  # 50 Hz para el servo

# Iniciar PWM de los motores y servos
motor2.start(0)
motor3.start(0)
motor4.start(0)
for pwm in pwms:
    pwm.start(7.5)  # 7.5% es la señal de parada para un servo continuo

# Archivo donde se guarda la detección
archivo_resultado = "/home/ra/yolo/deteccion.txt"

# -------------------- FUNCIONES --------------------
def set_servo_angle(pwm, angle):
    """Mueve un servo a un ángulo entre 0° y 180°."""
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Detiene vibración

def activar_motor3():
    """Activa motor3 moviéndolo de 0° a 180° usando PWM."""
    print("Activando motor3...")
    motor3.ChangeDutyCycle(2.5 + (180 / 180.0) * 10)
    time.sleep(1)  # Asegúrate de que se mueve a la posición correcta
    motor3.ChangeDutyCycle(2.5 + (0 / 180.0) * 10)
    time.sleep(1)
    print("Motor3 activado (180°).")

def desactivar_motor3():
    """Desactiva motor3 regresando a 0°."""
    print("Desactivando motor3...")
    motor3.ChangeDutyCycle(2.5 + (180 / 180.0) * 10)
    time.sleep(1)
    print("Motor3 desactivado (0°).\n")

def activar_motor2():
    """Activa y desactiva el motor2."""
    print("Activando motor2...")
    set_servo_angle(motor2, 0)     # Activa
    time.sleep(0.5)
    set_servo_angle(motor2, 90)   # Detiene
    print("Motor2 desactivado.\n")
    
def activar_motor4():
    """Activa motor4 moviéndolo de 0° a 180° usando PWM."""
    print("Activando motor4...")
    motor4.ChangeDutyCycle(2.5 + (0 / 180.0) * 10)
    time.sleep(1)
    motor4.ChangeDutyCycle(2.5 + (180 / 180.0) * 10)
    time.sleep(1)
    print("Motor4 activado (180°).")

def desactivar_motor4():
    """Desactiva motor4 regresando a 0°."""
    print("Desactivando motor4...")
    motor4.ChangeDutyCycle(2.5 + (0 / 180.0) * 10)
    time.sleep(1)
    print("Motor4 desactivado (0°).\n")

def set_continuous_servo(pwm, speed):
    """Controla el motor1: velocidad de -100 a 100."""
    duty = 7.5 + (speed / 100) * 2.5  # Ajuste para controlar el servo
    pwm.ChangeDutyCycle(duty)
    print(f"Controlando motor1 a {speed}% velocidad (DutyCycle: {duty})")

def leer_resultado():
    if not os.path.exists(archivo_resultado):
        print(f"No se encuentra el archivo {archivo_resultado}")
        return None

    with open(archivo_resultado, "r") as f:
        deteccion = f.read().strip().lower()

    print(f"Contenido del archivo: {deteccion}")
    return deteccion

# -------------------- BUCLE PRINCIPAL --------------------
if __name__ == "__main__":
    deteccion_anterior = None  # Variable para almacenar la detección anterior
    contador_detecciones = 0   # Contador de detecciones consecutivas

    try:
        while True:
            deteccion = leer_resultado()

            if deteccion is None:
                time.sleep(0.5)
                continue  # Si no se detectó ningún valor válido, seguir esperando

            if deteccion == deteccion_anterior:
                contador_detecciones += 1
            else:
                contador_detecciones = 1  # Si cambia la detección, reiniciamos el contador

            if contador_detecciones >= 2:
                # Solo ejecutamos la secuencia si la detección se repitió dos veces
                if deteccion == "inmaduro":
                    # Secuencia: motor3 → motor2 → motor3
                    activar_motor3()
                    time.sleep(0.25)
                    activar_motor2()
                    time.sleep(0.25)
                    desactivar_motor3()
                    time.sleep(0.25)

                elif deteccion == "maduro":
                    activar_motor4()
                    time.sleep(0.25)
                    activar_motor2()
                    time.sleep(0.25)
                    desactivar_motor4()
                    time.sleep(0.25)

                # Después de las condiciones, activamos y desactivamos motor1 (al final)
                print("Activando motor1...")
                set_continuous_servo(pwms[0], -70)  # Activar motor1 (50% velocidad hacia adelante)
                time.sleep(0.68)  # Mantenerlo 3 segundos
                set_continuous_servo(pwms[0], 0)   # Detener motor1
                pwm.ChangeDutyCycle(0)  # Detiene vibración
                time.sleep(5)
                print("Motor1 detenido.")

                # Resetear el contador y la detección para evitar ejecutar la secuencia varias veces
                contador_detecciones = 0

            deteccion_anterior = deteccion
            

    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")

    finally:
        # Detener PWM y limpiar GPIO al finalizar
        motor2.stop()
        motor3.stop()
        motor4.stop()
        for pwm in pwms:
            pwm.stop()
        GPIO.cleanup()
        print("GPIO liberado. Programa finalizado.")
