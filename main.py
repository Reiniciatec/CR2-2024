import cyberpi as cy
from cyberpi import mbot2 as m 
import time

# Varibles globales
vMotor = 15
vMotorGiro = 7

def line_follower():
    """
    Función que hace que el robot siga una línea.
    """
    offset = cy.quad_rgb_sensor.get_offset_track(index = 1)  # Obtenemos el offset
    speed_adjustment = offset  # Ajustamos la velocidad basándonos en el offset

    # Configuramos la velocidad de los motores
    motor_right_speed = -vMotor + ((speed_adjustment/2)*-1)  # Ajustamos la velocidad del motor derecho
    motor_left_speed = vMotor + ((speed_adjustment/2)*-1)  # Ajustamos la velocidad del motor izquierdo

    # Controlamos los motores
    m.drive_speed(motor_left_speed, motor_right_speed)

@cy.event.is_press("a")
def main():
    sLinea()
