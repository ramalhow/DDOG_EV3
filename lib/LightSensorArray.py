from micropython import const
#from pybricks.iodevices import Ev3devSensor
from pybricks.iodevices  import I2CDevice

LSA_DEFAULT_ADDRESS         = const(0x14)
LSA_COMMAND                 = const(0x41)
LSA_CALIBRATED              = const(0x42)
LSA_UNCALIBRATED            = const(0x6A)
LSA_WHITE_LIMIT             = const(0x4A)
LSA_BLACK_LIMIT             = const(0x52)
LSA_WHITE_CALIBRATION_DATA  = const(0x5A)
LSA_BLACK_CALIBRATION_DATA  = const(0x62)

class LSA(): #Ev3devSensor):

    def __init__(self, port):

        # Inicializa a interface do Ev3dev (classe pai) 
        #super().__init__(port)

        # Incializa o sensor também como dispositivo I2C
        self.device_addres = LSA_DEFAULT_ADDRESS
        self.i2c_device = I2CDevice(port, LSA_DEFAULT_ADDRESS >>1)

        # Define o caminho do sensor no sysfs path
        #self.path = '/sys/class/lego-sensor/sensor' + str(self.sensor_index)
    '''
    def get_commands(self):
        with open(self.path + '/commands', 'r') as m:

            # Read the contents.
            contents = m.read()

            # Strip the newline symbol, and split at every space symbol.
            return contents.strip().split(' ')

    '''

    def send_command(self, cmd) -> None:
        self.i2c_device.write(reg=LSA_COMMAND, data=cmd)

    def get_data(self, address, size) -> bytearray | None:
        data = self.i2c_device.read(address, size)
        return (data)
    
    def calibrate_white(self) -> None:
        self.send_command(b'W')

    def calibrate_black(self) -> None:
        self.send_command(b'B')

    def read_calibrated(self):
        return [x for x in self.get_data(LSA_CALIBRATED, 8)]

    # TODO: fazer a leitura do valor 'cru' das tensões de cada sensor
    # aparentemente, os index impares são sempre 0
    def read_raw(self) -> tuple:
        s = self.get_data(LSA_UNCALIBRATED, 16)
        return [i for i in s]

    def get_white_limit(self) -> bytearray | None:
        return [x for x in self.get_data(LSA_WHITE_LIMIT, 8)]

    def get_black_limit(self) -> bytearray | None:
        return [x for x in self.get_data(LSA_BLACK_LIMIT, 8)]

    def get_white_calibration_data(self) -> bytearray | None:
        return [x for x in self.get_data(LSA_WHITE_CALIBRATION_DATA, 8)]

    def get_black_calibration_data(self) -> bytearray | None:
        return [x for x in self.get_data(LSA_BLACK_CALIBRATION_DATA, 8)]
        