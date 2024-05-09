import cyberpi as cy
from cyberpi import mbot2 as m 
import time

# Varibles globales
vMotor = 15
vMotorGiro = 7

def sLinea ():
    while (True):
        # L1 Es TRUE si se esta viendo, caso contrario es FALSE
        l1 = not cy.quad_rgb_sensor.is_line("L1", 1)
        
        # R1 Es TRUE si se esta viendo, caso contrario es FALSE
        r1 = not cy.quad_rgb_sensor.is_line("R1", 1)
        
        # Avanzar hacia adelante
        if l1 and r1: # L1 TRUE and R1 TRUE
            m.drive_power(vMotor, -vMotor)
           
        # Girar a la izquierda
        elif l1 and not r1: #L1 TRUE and R1 FALSE
            m.drive_power(0, -vMotor)
           
        # Girar a la derecha
        elif not l1 and r1: # L1 FALSE and R1 TRUE
            m.drive_power(vMotor, 0)
           
        # No observa linea
        else: # L1 FALSE and R1 FALSE
            m.drive_power(0, 0)

@cy.event.is_press("a")
def main():
    sLinea()
