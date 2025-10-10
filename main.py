#!/usr/bin/env pybricks-micropython
import math
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Direction, Button
from pybricks.robotics import DriveBase

left_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
right_motor = Motor(Port.D, positive_direction=Direction.CLOCKWISE)

sensorL = ColorSensor(Port.S4)
sensorR = ColorSensor(Port.S1)

#robot = DriveBase(left_motor,right_motor, wheel_diameter = 55.5, axle_track=104)

vel = 300
BLACK_LIMIT = 15

target = 0
sample_time = 0.10 # em segundos

kP =25#7
kI = 0
kD = 0

proporcional = 0
derivativo = 0
integral = 0

maxIntegral = 10
minIntegral = -10

lastError = 0
lastMeasurement = 0

def update(measurement):
    global proporcional, integral, derivativo, kP, kI, kD, maxIntegral, minIntegral, lastError, lastMeasurement, sample_time

    erro = target - measurement
    
    proporcional = kP * erro

    integral += (0.5 * kI * sample_time * (erro + lastError) )

    integral = max(integral, maxIntegral)
    integral = min(integral, minIntegral)

    # todo: fazer filtro passa-baixa
    derivativo += -2.0 * kD * (measurement - lastMeasurement)

    lastError = erro
    lastMeasurement = measurement

    out = proporcional #+ integral + derivativo
    return out

while True:

    reflectionR = sensorR.reflection()
    reflectionL = sensorL.reflection()

    color = reflectionL - reflectionR

    signal = update(color)

    print('sensorL: ', reflectionL)
    print('sensorR: ', reflectionR)

    left_motor.run(vel + signal)
    right_motor.run(vel - signal)

    print('motorL ', left_motor.speed())
    print('motorR ', right_motor.speed())