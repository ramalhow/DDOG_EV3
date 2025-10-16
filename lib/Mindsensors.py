from micropython import const
from pybricks.iodevices  import I2CDevice

LSA_DEFAULT_ADDRESS         = const(0x14)

LSA_COMMAND                 = const(0x41)

LSA_CALIBRATED              = const(0x42)

LSA_UNCALIBRATED            = const(0x6A)

LSA_WHITE_LIMIT             = const(0x4A)

LSA_BLACK_LIMIT             = const(0x52)

LSA_WHITE_CALIBRATION_DATA  = const(0x5A)

LSA_BLACK_CALIBRATION_DATA  = const(0x62)

class LightSensorArray:
    device_address = 0

    def __init__(self, port, address=LSA_DEFAULT_ADDRESS):
        self.port = port
        self.device_addres = address
        self.i2c_device = I2CDevice(port, address>>1)

    def get_data(self, address, size) -> bytearray | None:
        data = self.i2c_device.read(address, size)
        return (data)

        '''
        try:
            data = self.i2c_device.read(address, size)
            return bytearray(data)

        except OSError:
            print("ERROR: falha na comunicação com o dispositivo I2C, verifique os cabos do sensor e a entrada correspondente.")
        '''

    def send_command(self, cmd) -> None:
        self.i2c_device.write(reg=LSA_COMMAND, data=cmd)

    ## Calibrates the white value for the LightSensorArray
    #  @param self The object pointer.
    def calibrate_white(self) -> None:
        self.send_command(b'W')

    ## Calibrates the black value for the LightSensorArray
    #  @param self The object pointer.
    def calibrate_black(self) -> None:
        self.send_command(b'B')

    ## Wakes up or turns on the LEDs of the LightSensorArray
    #  @param self The object pointer.
    def wakeup(self) -> None:
        self.send_command(b'P')

    ## Puts to sleep, or turns off the LEDs of the LightSensorArray
    #  @param self The object pointer.
    def goto_sleep(self) -> None:
        self.command(b'D')

    def read_calibrated(self) -> bytearray | None:
        arr = [x for x in self.get_data(LSA_CALIBRATED, 8)]
        return arr

    def get_raw_voltages(self) -> bytearray | None:
        s = self.get_data(LSA_UNCALIBRATED, 16)
        array = [i for i in s]

        '''
        for i in range(0, 16, 2):
            value = (s[i] << 8) | s[i+1]
            array.append(value)
        '''

        return array

    def get_white_limit(self) -> bytearray | None:
        arr = [x for x in self.get_data(LSA_WHITE_LIMIT, 8)]
        return arr

    def get_black_limit(self) -> bytearray | None:
        arr = [x for x in self.get_data(LSA_BLACK_LIMIT, 8)]
        return arr

    def get_white_calibration_data(self) -> bytearray | None:
        arr = [x for x in self.get_data(LSA_WHITE_CALIBRATION_DATA, 8)]
        return arr

    def get_black_calibration_data(self) -> bytearray | None:
        arr = [x for x in self.get_data(LSA_BLACK_CALIBRATION_DATA, 8)]
        return arr