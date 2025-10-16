#!/usr/bin/env pybricks-micropython



# Parâmetros de otimzação do micropython
from micropython import const, opt_level

# Imports locais
from lib.PIDController import PIDController
#from lib.LightSensorArray import LSA

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
right_motor = Motor(Port.D)
robot = DriveBase(left_motor, right_motor, wheel_diameter=45.0, axle_track=255)

# Sensores
sensorR = ColorSensor(Port.S4)
sensorL = ColorSensor(Port.S1)

ultra = UltrasonicSensor(Port.S3)

# Parâmetros do controlador PID
KP = 4
KI = const(0)
KD = const(0)
controller = PIDController(KP, KI, KD)

# Parâmetros chassi/drivebase
BASE_VEL = const(150)
DESVIO_RIGHT = 0
DESVIO_LEFT = 0

# Parâmetros sensor de cor
LIMIAR_PRETO = const(10)
LIMIAR_BRANCO = const(60)

# Parâmetros ultrasônico
DIST_ULTRASONICO = const(100) # em milimetros

# Parâmetros do sensor LSA
USAR_SENSOR_LSA = False
LIMIAR_PRETO_LSA = const(80)
PESOS_LSA = [1, 2, 3, 4, -4, -3, -2, -1]

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


def check_curvas90_teste(colorLeft, colorRight):
    
    # curva 90° para a esquerda
    if( (colorLeft <= LIMIAR_PRETO) and (colorRight >= LIMIAR_BRANCO) ):
        right_motor.run_angle(100, 80, wait=False)
        left_motor.run_angle(100, 80, wait=True)
        right_motor.run_angle(100, 165, wait=False)
        left_motor.run_angle(100, -165, wait=True)
        wait(200)
    elif( (colorRight <= LIMIAR_PRETO) and (colorLeft >= LIMIAR_BRANCO) ):
        right_motor.run_angle(100, 80, wait=False)
        left_motor.run_angle(100, 80, wait=True)
        right_motor.run_angle(100, -165, wait=False)
        left_motor.run_angle(100, 165, wait=True)
        wait(200)

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