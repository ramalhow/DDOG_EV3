#!/usr/bin/env pybricks-micropython

import math
from lib.PIDController import PIDController
from lib.LightSensorArray import LSA

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.media.ev3dev import Font

ev3 = EV3Brick()
ev3.screen.set_font(Font(size=14))

# Atuadores
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

robot = DriveBase(left_motor, right_motor, wheel_diameter=45.0, axle_track=255)

# Sensores
sensorL = ColorSensor(Port.S4)
sensorR = ColorSensor(Port.S1)

#lsa = LSA(Port.S2)
ultra = UltrasonicSensor(Port.S3)

# Configurações e Parâmetros
KP = const(25)
KI = const(0)
KD = const(5)
controller = PIDController(KP, KI, KD)

BASE_VEL = const(300)
LIMIAR_PRETO = const(25)
LIMIAR_BRANCO = const(90)

DIST_ULTRASONICO = const(100) # em milimetros

USAR_SENSOR_LSA = False
LIMIAR_PRETO_LSA = const(80)
PESOS_LSA = [1, 2, 3, 4, -4, -3, -2, -1]

# Funções principais

'''
TODO: fazer os comandos de calibração do sensor LSA funcionarem
def loop_calibracao():
    while True:
        buttons = ev3.buttons.pressed()
        ev3.screen.print("MODO: CALIBRAÇÃO")
        wait(500)

        if Button.UP in buttons:
            lsa.calibrate_white()
            ev3.screen.print("CALIBRAÇÃO: branco calibrado")
            ev3.screen.print("novo limite de branco: ", )
            wait(2000)

        if Button.DOWN in buttons:
            lsa.calibrate_black()
            ev3.screen.print("CALIBRAÇÃO: preto calibrado")
            ev3.screen.print("novo limite de preto: ", )
            wait(2000)

        if Button.CENTER in buttons:
            print("CALIBRAÇÃO: Saindo da calibração")
            wait(1000)
            break
        
        ev3.screen.clear()
'''

def check_ultrasonico():

    if(ultra.distance() < DIST_ULTRASONICO):
        ev3.speaker.beep(200, 500)
        robot.stop()
        
        # pega a direita e se alinha em paralelo com o objeto
        robot.straight(-200)
        robot.turn(90)
        robot.straight(200)
        robot.turn(-90)

        # tendo o objeto fora da frente do robô, iremos desviar
        robot.straight(600)
        robot.stop()
        robot.turn(-90)
        robot.straight(200)
        robot.turn(90)

        # deu tudo certo, o robô está de costas com o obstáculo
        robot.straight(100)


def check_curvas90(colorLeft, colorRight):
    
    # curva 90° para a esquerda
    if( (colorLeft <= LIMIAR_PRETO) and (colorRight >= LIMIAR_BRANCO) ):
        ev3.speaker.beep(157, 200)
        robot.stop()
        robot.straight(-100)
        robot.stop()
        robot.straight(100)

        color_right = sum(sensorR.rgb())

        for i in range(200):
            color_right = sum(sensorR.rgb())

        while True:
            color_right = sum(sensorR.rgb())

            if(color_right <= LIMIAR_PRETO):
                break
            else:
                robot.drive(0, 20)

    '''
    # curva 90° para a direita
    if ( (colorLeft >= LIMIAR_BRANCO) and (colorRight <= LIMIAR_PRETO) ):
        ev3.speaker.beep(157, 200)
        robot.stop()

        while True:
            color_left = sum(sensorL.rgb())

            if(color_left <= LIMIAR_PRETO):
                break
            else:
                robot.drive(0, 20)
    '''

def calcular_erro_lsa():
    soma_ponderada = 0
    soma_ativacoes = 0

    leitura = lsa.read_calibrated()

    for i in range(8):

        # invertemos o resultado da leitura do sensor:
        # maior o número == mais próximo do preto, logo tem maior peso
        ativacao = 100 - leitura[i]

        soma_ponderada += ativacao * PESOS_LSA[i]
        soma_ativacoes += ativacao

        # TODO: colocar um limiar pra detectar/filtrar os valores
        #if ativacao > LIMIAR_PRETO_LSA: -> se for verdade, consideramos a linha como preta

    # TODO: evitar divisão por 0 na soma das ativações
    return soma_ponderada / (soma_ativacoes + 1)

while True:
    
    # loop de calibração dos sensores
    #loop_calibracao()

    # main loop

    #check_ultrasonico()

    #reflectionL = sensorL.reflection()
    #reflectionR = sensorR.reflection()

    rgb_left = sum(sensorL.rgb())
    rgb_right = sum(sensorR.rgb())

    check_curvas90(rgb_left, rgb_right)

    if USAR_SENSOR_LSA:
        erro_lsa = calcular_erro_lsa()

        signal = controller.update(0, erro_lsa)

        print(erro_lsa)
        print(signal)

    else:
        color = rgb_left - rgb_right

        signal = controller.update(0, color)
        
        #print(color)
        #print(signal)
        
        #robot.drive(BASE_VEL, signal)

        print("left: {} // right: {} // erro: {}".format(rgb_left, rgb_right, color))