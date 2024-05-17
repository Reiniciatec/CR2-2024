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


def sLinea():
    # Obtiene la desviación del sensor
    offset = cy.quad_rgb_sensor.get_offset_track(index=1)
    cy.console.println(offset)

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


###########################################################
######################## Stage 1 ##########################
###########################################################


def s1PosicionInicial():
    m.servo_set(150, brazo)  # Posicion inicial brazo
    m.servo_set(145, mano)  # Posicion inicial mano


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
    time.sleep(0.5)
    m.servo_set(150, brazo)


@cy.event.receive("s1BIterativo")
def s1BIterativo():
    contador = 0
    while (4 > contador):
        m.servo_set(50, brazo)

        time.sleep(0.5)
        m.servo_set(140, brazo)
        contador += 1

        time.sleep(0.3)


@cy.event.receive("s1Oscilacion")
def s1Oscilacion():
    contador = 0
    while (2 > contador):
        m.drive_power(-vMotor/2, -vMotor/2)
        time.sleep(1)
        m.drive_power(vMotor/2, vMotor/2)
        time.sleep(1)
        contador += 1
    m.drive_power(-vMotor/2, -vMotor/2)
    time.sleep(0.5)
    m.drive_power(0, 0)


def s1TomaLapiz():
    cy.broadcast("s1AMano")
    while (cy.ultrasonic2.get() >= 7 or cy.ultrasonic2.get() == 300):
        m.drive_power(vMotorGiro, -vMotorGiro)

    m.drive_power(0, 0)
    m.servo_set(150, mano)


def s1MoverServoDespacio(servo, inicio, fin, paso=10, tiempo=0.5):
    # Mueve el servo a la posición inicial
    m.servo_set(inicio, servo)
    # Espera medio segundo para que el servo llegue a la posición
    time.sleep(tiempo)

    # Determina la dirección del movimiento
    if inicio > fin:
        paso = -abs(paso)
    else:
        paso = abs(paso)

    # Mueve el servo a la posición final en pasos
    for posicion in range(inicio, fin, paso):
        m.servo_set(posicion, servo)
        # Espera un poco entre cada paso para un movimiento lento y suave
        time.sleep(tiempo)

    # Libera el servo
    # m.servo_release(servo)


def s1Pizarra():
    cy.broadcast("s1BIterativo")
    cy.broadcast("s1Oscilacion")


@cy.event.is_press("b")
def main2():
    s1MoverServoDespacio(servo=brazo, inicio=150, fin=90, paso=2, tiempo=0.1)


@cy.event.is_press("up")
def mainb():
    while True:
        sLinea()
    # angulo = m.servo_get(brazo)
    # cy.console.println(angulo)


@cy.event.is_press("a")
def main():
    s1PosicionInicial()
    while True:

        sLinea()

    # @cy.event.is_press("a")
    # def main():
    #     s1PosicionInicial()
    #     s1ALinea()
    #     cy.broadcast("s1Brazo")
    #     while (True):
    #         color = cy.quad_rgb_sensor.is_color("b", "any", 1)
    #         if color:
    #             m.drive_power(0, 0)
    #             break
    #         sLinea()
    #     s1TomaLapiz()
    #     s1Girar(direccion="izquierda", tiempo=1)
    #     s1Pizarra()
    #     time.sleep(5)
    #     s1Girar(direccion="derecha", tiempo=1)
    #     sLinea()
