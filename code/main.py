import cyberpi as cy
from cyberpi import mbot2 as m 
import time

# Varibles globales
vMotor = 30
vMotorGiro = 15

# Servomotores
brazo = 2
mano = 1

###########################################################
################## Funciones globales #####################
###########################################################


def sLinea ():
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


###########################################################
######################## Stage 1 ##########################
###########################################################


def s1PosicionInicial():
    m.servo_set(150, brazo) # Posicion inicial brazo
    m.servo_set(145, mano) # Posicion inicial mano


def s1ALinea():
    while (True):
        l1 = not cy.quad_rgb_sensor.is_line("L1", 1)
        r1 = not cy.quad_rgb_sensor.is_line("R1", 1)
        
        if not l1 and not r1:
            m.drive_power(vMotor, -vMotor)
        else:
            break

def s1Avanzar(esperar):
    m.drive_power(vMotor, -vMotor)
    time.sleep(esperar)
    m.drive_power(0, 0)

@cy.event.receive("s1AMano")
def s1AMano():
     m.servo_set(0, mano)

@cy.event.receive("s1Brazo")
def s1Brazo():
    m.servo_set(50, brazo)
    time.sleep(0.2)
    m.servo_set(150, mano)

def s1TomaLapiz():
    cy.broadcast("s1AMano") 
    while (cy.ultrasonic2.get() != 300):
        cy.console.println(cy.ultrasonic2.get())
        m.drive_power(vMotor, -vMotor)
    m.drive_power(0, 0)
    m.servo_set(150, mano)

@cy.event.is_press("a")
def main():
    s1PosicionInicial()
    s1ALinea()
    cy.broadcast("s1Brazo") 
    while (True):
        color = cy.quad_rgb_sensor.is_color("b","any", 1)
        if color:
            m.drive_power(0, 0)
            break
        sLinea()
    
    s1TomaLapiz()

    
    
 # cy.broadcast("subir_cuello_async")  
 # @cy.event.receive("subir_cuello_async")
    