import cyberpi as cy
from cyberpi import mbot2 as m
import time

# Variables globales
vMotor = 40
vMotorGiro = 6
brazo = 2
mano = 1

def execute_until(task, condition):
    """
    Ejecuta la tarea repetidamente hasta que la condición sea verdadera.

    :param task: Función a ejecutar repetidamente.
    :param condition: Función que retorna True si se cumple la condición de parada.
    """
    while True:
        task()
        if condition():
            break
        time.sleep(0.1)  # Añadir un pequeño retraso para evitar un bucle muy rápido

def detect_color(color, sensor_index=1) -> bool:
    """
    Detecta si un color específico está presente usando el sensor de color.
    
    :param color: El color a detectar (yellow y, green g, cyan c, red r, blue b, purple p, white w, black k).
    :param sensor_index: El índice del sensor a usar.
    :return: True si el color es detectado, False en caso contrario.
    """
    return cy.quad_rgb_sensor.is_color(color, "any", sensor_index)
    
def detect_distance(threshold, sensor_index=1):
    """
    Detecta si la distancia medida por el sensor ultrasónico está por debajo de un umbral.

    :param threshold: La distancia umbral para detección.
    :param sensor_index: El índice del sensor ultrasónico a usar.
    :return: True si la distancia es menor o igual al umbral, False en caso contrario.
    """
    distance = cy.ultrasonic2.get(sensor_index)
    return distance <= threshold and distance != 300
    
def line_follower():
    """
    Función que hace que el robot siga una línea.
    """
    offset = cy.quad_rgb_sensor.get_offset_track(index=1)  # Obtenemos el offset
    speed_adjustment = offset  # Ajustamos la velocidad basándonos en el offset

    # Configuramos la velocidad de los motores
    motor_right_speed = -vMotor + ((speed_adjustment / 2) * -1)  # Ajustamos la velocidad del motor derecho
    motor_left_speed = vMotor + ((speed_adjustment / 2) * -1)  # Ajustamos la velocidad del motor izquierdo

    # Controlamos los motores
    m.drive_speed(motor_left_speed, motor_right_speed)

def ultrasonicLight(emotion):
    """
    Funcion para encender las luces del ultrasonido
    :param: La emocion a utilizar (sleepy, happy, dizzy, wink, thinking)
    """
    
    cy.ultrasonic2.play(emotion, index =1)


def moverServoDespacio(servo, inicio, fin, paso=10, tiempo=0.5):
    """
    Mueve el servo desde la posición inicial a la posición final en pasos,
    esperando un tiempo específico entre cada paso para un movimiento lento y suave.
    """
    m.servo_set(inicio, servo)
    time.sleep(tiempo)

    paso = abs(paso) if inicio < fin else -abs(paso)
    
    for posicion in range(inicio, fin, paso):
        m.servo_set(posicion, servo)
        time.sleep(tiempo)
    
    m.servo_set(fin, servo)  # Asegurarse de que el servo llega a la posición final
    m.servo_release(servo)



@cy.event.receive("pensamiento")
def pensamiento():
    for i in range(4):
        cy.broadcast("pensamiento2")
        ultrasonicLight("thinking")
        
@cy.event.receive("pensamiento2")
def pensamiento2():
   cy.led.play("meteor_blue")

@cy.event.receive("eureka_emotions")
def eureka_emotion():
        for i in range(4):
            cy.ultrasonic2.play("happy", 1)
            cy.led.play("rainbow")
            
            
def ePizarra():
    m.servo_set(150, mano)
    t_espera = 0.5
    ct_espera = 3
    for i in range(2):
        # Subir brazo
        m.servo_set(30, brazo)
        time.sleep(t_espera)
        
        moverServoDespacio(servo=mano, inicio=100, fin=30, paso=10, tiempo=0.1)
        time.sleep(t_espera)
        
        # Bajar brazo
        m.servo_set(150, brazo)
        time.sleep(t_espera)
        
        m.servo_set(150, mano)
    
        time.sleep(t_espera*ct_espera)
        
def ePizarraConPlumon():

    t_espera = 0.5

    for i in range(2):
        # Subir brazo
        m.servo_set(30, brazo)
        time.sleep(t_espera)
        
        # Bajar brazo
        m.servo_set(150, brazo)
        time.sleep(t_espera)

def eEuphoria():
    # Impacto (Llega la idea)
    cy.broadcast("eureka_emotions")
    cy.audio.play("start")
    m.servo_set(30, brazo)
    m.servo_set(50, mano)
    
    # Tiempo procesando su genialidad
    time.sleep(1)
    
    # Reaccion
    moverServoDespacio(servo=mano, inicio=50, fin=150, paso=15, tiempo=0.2)
    m.servo_set(150, brazo)


def eureka():
    # Impacto de su maravillosa idea
    eEuphoria()
    
    # Girar hacia la pizarra
    m.drive_power(0, -50)
    time.sleep(0.6)    
    m.drive_power(0, 0)
    
    time.sleep(1)
    
    # Observar la pizarra
    ePizarra()
    
    # Retroceder hasta estar preparado para tomar la luz
    m.drive_power(-60, 80)
    time.sleep(0.6)
    m.drive_power(0, 0)
    
    time.sleep(0.2)
    
   
    # Acercarse a tomar la luz
    m.servo_set(30, mano)
    while (cy.ultrasonic2.get(1) >= 5):
        m.drive_power(30, -30)
    
    time.sleep(0.15)
    
    m.drive_power(0,0)
    
    # Tomar la luz
    m.servo_set(120, mano)
    cy.audio.play("start")
    time.sleep(0.5)
    
    m.drive_power(20, 20)
    time.sleep(0.4)
    m.drive_power(0,0)
    
    # Alzar la luz
    m.servo_set(40, brazo)
    
    cy.broadcast("eureka_emotions")
    time.sleep(2)
    
    # Bajar la luz
    m.servo_set(150, brazo)
    
    # Darce la vuelta para poder ir a dejar la ampolleta
    m.drive_power(80, 80)
    time.sleep(0.7)
    m.drive_power(0, 0)
    
    

    # Avanzar brevemente para depositar la luz
    m.drive_power(40, -35)
    time.sleep(0.7)
    m.drive_power(0, 0)
    
    m.servo_set(30, mano)
    
    
    
def tPlumon():
    # Abrir mano y tomar plumon
    m.servo_set(30, mano)
    
    m.drive_power(40, 60)
    time.sleep(0.2)
    m.drive_power(0, 0)
    
    m.drive_power(20, -20)
    time.sleep(1)
    m.drive_power(0, 0)
    
    m.servo_set(80, brazo)
    
    time.sleep(0.1)
    m.servo_set(150, mano)
    
    time.sleep(0.1)
    
    m.servo_set(30, brazo)
    
def rPizarra():
    # Girar hacia la pizzara
    m.drive_power(-40,20)
    time.sleep(0.05)
    
    # avanzar hacia la pizarra
    m.drive_power(40,40)
    time.sleep(0.4)
    m.drive_power(0,0)
    
    m.drive_power(40,-40)
    time.sleep(0.3)
    m.drive_power(0,0)
    
    ePizarraConPlumon()
    
    m.drive_power(50,50)
    time.sleep(0.5)
    m.drive_power(0,0)
    
    m.drive_power(30,-30)
    time.sleep(1)
    m.drive_power(0,0)
    


def eAvanzar(velocidad: int, tiempo: float):
    m.drive_power(velocidad, -velocidad)
    time.sleep(tiempo)
    m.drive_power(0, 0)


def ideacion():
    # Despertar y estirarse
    cy.led.on(0,0,255)
    ultrasonicLight("sleepy")
    moverServoDespacio(brazo, 150, 50, 5, 0.2)  
    
    ultrasonicLight("sleepy")
    moverServoDespacio(mano, 145, 50, 10, 0.1)
    
    
    cy.broadcast("pensamiento")
    s1PosicionInicial()

        
def main():
    """
    Función principal que usa execute_until para seguir la línea hasta que se detecte un color específico.
    """
    
    # s1PosicionInicial()
    # ideacion()
    # eAvanzar(velocidad=40, tiempo=0.6)
    
    # Seguir la línea hasta detectar el color azul
    execute_until(task=line_follower, condition=lambda: detect_color("blue"))
    m.drive_power(0, 0)
    
    eureka()
    
    tPlumon()
    
    rPizarra()
    
def s1PosicionInicial():
    """
    Coloca los servos en la posición inicial.
    """
    m.servo_set(150, brazo)
    m.servo_set(145, mano)

@cy.event.is_press("a")
def start_main():
    """
    Inicia la función principal al presionar el botón 'a'.
    """
    main()
    
@cy.event.is_press("b")
def debug():
    """
    Inicia la funcion para debuggear caracteristicas en especifico del programa
    """
    m.drive_power(0, -60)

    # tPlumon()
    # # eureka()
    # cy.console.println(cy.ultrasonic2.get(1))
  
    
# Comienza el programa
cy.console.println("Programa iniciado. Presiona 'a' para empezar.")
