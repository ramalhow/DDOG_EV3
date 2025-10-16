#!/usr/bin/env pybricks-micropython



# Parâmetros de otimzação do micropython
from micropython import const, opt_level

# Imports locais
from lib.PIDController import PIDController
from lib.LightSensorArray import LSA

# Imports globais 
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.media.ev3dev import Font

# Equivalente de "compilar" usando a flag -O3
opt_level(3)

ev3 = EV3Brick()
ev3.screen.set_font(Font(size=14))

# Atuadores
left_motor = Motor(Port.A)
right_motor = Motor(Port.C)
robot = DriveBase(left_motor, right_motor, wheel_diameter=45.0, axle_track=255)

# Sensores
sensorR = ColorSensor(Port.S4)
sensorL = ColorSensor(Port.S1)

lsa = LSA(Port.S3)
ultra = UltrasonicSensor(Port.S2)

# Parâmetros do controlador PID
KP = 6
KI = const(0)
KD = const(0)
controller = PIDController(KP, KI, KD)

# Parâmetros chassi/drivebase
BASE_VEL = const(150)
DESVIO_RIGHT = 6
DESVIO_LEFT = 0

# Parâmetros sensor de cor
LIMIAR_PRETO = const(15)
LIMIAR_BRANCO = const(35)

# Parâmetros ultrasônico
DIST_ULTRASONICO = const(100) # em milimetros

# Parâmetros do sensor LSA
USAR_SENSOR_LSA = False
LIMIAR_PRETO_LSA = const(80)
PESOS_LSA = [1, 2, 3, 4, -4, -3, -2, -1]

# Funções principais

#TODO: fazer os comandos de calibração do sensor LSA funcionarem
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

        # toda vez devemos terminar com robot.stop()
        # se não, não dá pra usar os motores individualmente sem o micropython crashar
        robot.stop()

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

    # toda vez devemos terminar com robot.stop()
    # se não, não dá pra usar os motores individualmente sem o micropython crashar
    robot.stop()

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

def check_curvas90_teste(colorLeft, colorRight):
    
    # curva 90° para a esquerda
    if( (colorLeft <= LIMIAR_PRETO) and (colorRight >= LIMIAR_BRANCO) ):
        left_motor.run_angle(250, 100, wait=False)
        right_motor.run_angle(250, -100, wait=True)

    elif( (colorRight <= LIMIAR_PRETO) and (colorLeft >= LIMIAR_BRANCO) ):
        #left_motor.run_angle(250, 215, wait=False)
        #right_motor.run_angle(250, -215, wait=True)
        left_motor.run_angle(250, 100, wait=False)
        right_motor.run_angle(250, -100 , wait=True)

def calcular_erro_lsa():
    soma_ponderada = 0
    soma_ativacoes = 0

    leitura = lsa.read_calibrated() # 0 a 100?

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

def main_loop():
    #check_ultrasonico()

    #rgb_left = sum(sensorL.rgb())
    #rgb_right = sum(sensorR.rgb())
    #loop_calibracao()
    colorR = sensorR.reflection()
    colorL = sensorL.reflection()

    #check_curvas90(rgb_left, rgb_right)

    if USAR_SENSOR_LSA:
        erro_lsa = calcular_erro_lsa()

        signal = controller.update(0, erro_lsa)

        #print(erro_lsa)
        #print(3*signal)
        print(lsa.read_calibrated())

        left_motor.run(BASE_VEL + 15*signal)
        right_motor.run(BASE_VEL - 15*signal)

        #print("left: {} // right: {} // erro: {}".format(colorL, colorR, color))

    else:
        color = (colorR + DESVIO_RIGHT) - (colorL + DESVIO_LEFT)

        signal = controller.update(0, color)

        check_curvas90_teste(colorL, colorR)

        left_motor.run(BASE_VEL + signal)
        right_motor.run(BASE_VEL - signal)



        print("left: {} // right: {} // erro: {}".format(colorL, colorR, color))



while True:
    #print(lsa.read_calibrated())
    # loop de calibração dos sensores
    #loop_calibracao()

    main_loop()