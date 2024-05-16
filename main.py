import cyberpi as cy
from cyberpi import mbot2 as m 
import time

# Varibles globales
vMotor = 15
vMotorGiro = 7

def sLinea():
    # Obtiene la desviación del sensor
    offset = cy.quad_rgb_sensor.get_offset_track(index=1)

    # Define la velocidad base del motor
    vMotor = 50  # Ajusta este valor según sea necesario

    # Ajusta la velocidad de los motores basado en la desviación
    if offset < -20:  # Desviación significativa a la izquierda
        m.drive_power(0, -vMotor)
    elif offset > 20:  # Desviación significativa a la derecha
        m.drive_power(vMotor, 0)
    else:  # Pequeña desviación o centrado
        m.drive_power(vMotor, -vMotor)

    # Detener si la desviación es extrema
    if offset <= -100 or offset >= 100:
        m.drive_power(0, 0)

@cy.event.is_press("a")
def main():
    sLinea()
