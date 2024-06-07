import cyberpi as cy
from cyberpi import mbot2 as m 
import time

# Varibles globales
vMotor = 15
vMotorGiro = 7

def smooth_servo_set(start_angle, end_angle, port, step=1, delay=0.02):
    # Determine the direction of movement
    if start_angle < end_angle:
        angle_range = range(start_angle, end_angle + 1, step)
    else:
        angle_range = range(start_angle, end_angle - 1, -step)
    
    for angle in angle_range:
        m.servo_set(angle, port)
        time.sleep(delay)

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
    while True:
        if cy.quad_rgb_sensor.is_color("g","L1",1) or cy.quad_rgb_sensor.is_color("g","R1",1) == True:
            smooth_servo_set(90,20,"s2")
            m.drive_power(vMotor,-vMotor)
            time.sleep(2.3)
            m.drive_power(vMotor,-vMotor)
            time.sleep(1)
            m.drive_power(0,0)
            time.sleep(0.5)
            for i in range(5):
                smooth_servo_set(30,70,"s2")
                smooth_servo_set(110,150,"s1")
            smooth_servo_set(90,40,"s2")
            m.drive_power(-vMotor,2*(vMotor))
            time.sleep(1.2)
            m.drive_power(30,0)
            time.sleep(1)
            m.drive_power(0,0)
            m.drive_power(vMotor,-vMotor)
            time.sleep(2.5)
            m.drive_power(0,0)
            smooth_servo_set(90,130,"s2")
            m.drive_power(0,-vMotor)
            time.sleep(2)
            m.drive_power(0,0)
            time.sleep(1)
            for i in range(3):
                smooth_servo_set(110,150,"s1")
            m.drive_power(-vMotor,-vMotor)
            time.sleep(2)
            m.drive_power(0,0)
            time.sleep(1)
            smooth_servo_set(90,150,"s1")
