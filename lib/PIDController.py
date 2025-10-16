from micropython import const
SAMPLE_TIME = 0.10 # em segundos
MAX_INTEGRAL = const(10)
MIN_INTEGRAL = const(-10)

class PIDController():

    def __init__(self, kp, ki, kd):
        self.kP = kp
        self.kI = ki
        self.kD = kd

        self.proporcional = 0
        self.derivativo = 0
        self.integral = 0
        self.lastError = 0
        self.lastMeasurement = 0

    def update(self, target, measurement):

        erro = target - measurement
        
        self.proporcional = self.kP * erro

        self.integral += (0.5 * self.kI * SAMPLE_TIME * (erro + self.lastError) )

        self.integral = max(self.integral, MAX_INTEGRAL)
        self.integral = min(self.integral, MIN_INTEGRAL)

        # todo: fazer filtro passa-baixa
        self.derivativo += self.kD * (measurement - self.lastMeasurement)

        self.lastError = erro
        self.lastMeasurement = measurement

        return self.proporcional + self.integral + self.derivativo