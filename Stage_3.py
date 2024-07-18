import cyberpi as cp
from cyberpi import mbot2 as m 
import time

def sLinea():
    offset = cp.quad_rgb_sensor.get_offset_track(index = 1)  # Obtenemos el offset
    speed_adjustment = offset  # Ajustamos la velocidad basándonos en el offset

    # Configuramos la velocidad de los motores
    motor_right_speed = -50 + ((speed_adjustment/2)*-1)  # Ajustamos la velocidad del motor derecho
    motor_left_speed = 50 + ((speed_adjustment/2)*-1)  # Ajustamos la velocidad del motor izquierdo

    # Controlamos los motores
    m.drive_speed(motor_left_speed, motor_right_speed)

# Datos de importancia
# Servo 2 = cuello
CUELLO_SUBIR = 70
CUELLO_BAJAR = 130
CUELLO_RANGO_MIN = 130
CUELLO_RANGO_MAX = 145
# Servo 1 = garra
GARRA_ABRIR = 45
GARRA_CERRAR = 145

# Funciones para mover servos con límites
def mover_servo(posicion, servo):
    m.servo_set(posicion, servo)

def mover_cuello(posicion):
    m.servo_set(posicion, 2)

def mover_garra(posicion):
    m.servo_set(posicion, 1)

# Funciones de movimiento
def mover_adelante(tiempo, velocidad=30):
    m.drive_speed(velocidad, -velocidad)
    time.sleep(tiempo)
    m.drive_speed(0, 0)

def mover_atras(tiempo, velocidad=30):
    m.drive_speed(-velocidad, velocidad)
    time.sleep(tiempo)
    m.drive_speed(0, 0)

def girar_izquierda(grados, velocidad=40):
    m.turn(-grados, velocidad)

def girar_derecha(grados, velocidad=30):
    m.turn(grados, velocidad)

# Evento para apretar teclas (bajar/subir cuello)
@cp.event.receive("apreta_teclas")
def aprieta_teclas():
    for _ in range(4):
        mover_cuello(CUELLO_RANGO_MAX)
        time.sleep(0.2)
        mover_cuello(CUELLO_RANGO_MIN)
        time.sleep(0.2)

# Evento para arreglar robot (bajar/subir cuello)
@cp.event.receive("arregla_robot")
def arregla_robot():
    for _ in range(2):
        mover_cuello(100)
        time.sleep(0.3)
        mover_cuello(80)
        time.sleep(0.3)

# Evento para bajar cuello
@cp.event.receive("bajar_cuello")
def bajar_cuello():
    mover_cuello(CUELLO_BAJAR)

# Evento para subir cuello
@cp.event.receive("subir_cuello")
def subir_cuello():
    mover_cuello(CUELLO_SUBIR)

# Evento para abrir garra
@cp.event.receive("abrir_garra")
def abrir_garra():
    mover_garra(GARRA_ABRIR)

# Evento para cerrar garra
@cp.event.receive("cerrar_garra")
def cerrar_garra():
    current_position = GARRA_ABRIR
    step = 5  # Ajusta el tamaño del paso según la velocidad deseada
    while current_position < GARRA_CERRAR:
        current_position += step
        if current_position > GARRA_CERRAR:
            current_position = GARRA_CERRAR
        mover_garra(current_position)
        time.sleep(0.1)  # Ajusta el tiempo de espera según la velocidad deseada

# Rutina completa v2 basada en detección de color rojo
@cp.event.receive("iniciar_rutinav2")
def iniciar_rutinav2():
        # Retrocede 0,5 segundos
        mover_atras(0.8)
        
        # Gira 20° izquierda
        girar_izquierda(45)
        time.sleep(0.5)
        
        # Apreta teclas
        cp.broadcast("apreta_teclas")
        time.sleep(2)
        
        # Gira 20° derecha
        girar_derecha(45)
        time.sleep(0.5)
        
        # Espera 1 segundo
        time.sleep(1)
        
        # Gira 20° izquierda
        girar_izquierda(45)
        time.sleep(0.5)
        
        # Apreta teclas
        cp.broadcast("apreta_teclas")
        time.sleep(2)
        
        # Gira 60° derecha
        girar_derecha(95)
        time.sleep(0.5)
        
        # Baja brazo mientras abre garra
        cp.broadcast("bajar_cuello")
        cp.broadcast("abrir_garra")
        time.sleep(1)
        
        # Avanza hasta que el sensor detecte algo cerca
        mover_adelante(1.7)
        
        # Cierra garra
        cp.broadcast("cerrar_garra")
        time.sleep(2)
        
        # Sube hasta el máximo 145
        mover_cuello(70)
        time.sleep(1)
        
        # Gira 45° izquierda
        girar_izquierda(100)
        time.sleep(0.5)
        
        # Avanza 1 segundo
        mover_adelante(1.4)
        
        # Baja 10 grados y sube a 145 dos veces
        for _ in range(2):
            mover_cuello(70 - 10)
            time.sleep(0.5)
            mover_cuello(70)
            time.sleep(0.5)
        
        # Retrocede
        mover_atras(1)
        time.sleep(1)
        
        # Espera 3 segundos
        time.sleep(1)
        
        # Retrocede
        mover_atras(1)
        time.sleep(1)
        
        # Gira 45° derecha
        girar_derecha(85)
        time.sleep(0.5)
        
        # Baja garra
        cp.broadcast("bajar_cuello")
        time.sleep(1)
        
        # Abre garra
        cp.broadcast("abrir_garra")
        time.sleep(1)
        
        # Retrocede 0,5 segundos
        mover_atras(0.5)
        
        # Gira 180° izquierda
        girar_izquierda(130)
        time.sleep(1)
        
        #avanza un poco para llegar al teclado 
        mover_adelante(1)
        time.sleep(1)
        
        # Apreta teclas
        cp.broadcast("apreta_teclas")
        cp.broadcast("cerrar_garra")
        time.sleep(2)
        
        # Para 0,5 segundos
        time.sleep(0.5)
        
        # Apreta teclas
        cp.broadcast("apreta_teclas")
        time.sleep(2)
        
        # Gira 100° derecha
        girar_derecha(80)
        time.sleep(1)
        
        # Avanza 1 segundo
        mover_adelante(2)
        
        # Sube hasta el máximo 145 y baja 10 grados dos veces
        for _ in range(2):
            mover_cuello(CUELLO_RANGO_MAX)
            time.sleep(0.5)
            mover_cuello(CUELLO_RANGO_MAX - 10)
            time.sleep(0.5)
        
        # Retrocede 1 segundo
        mover_atras(1)
        
        # Espera 1 segundo
        time.sleep(1)
        
        # Gira 360°
        girar_derecha(360)
        time.sleep(2)
        
        # Avanza 0,3 segundos
        mover_adelante(0.3)
        
        # Sigue línea
        sLinea()



@cp.event.is_press("a")
def main():
    sLinea()
    while True:
        color = cp.quad_rgb_sensor.is_color("r", "any", 1)
        if color:
            m.drive_power(0, 0)
            break
        sLinea()
    cp.broadcast("iniciar_rutinav2")
