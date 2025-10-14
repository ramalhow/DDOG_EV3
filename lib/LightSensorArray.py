from pybricks.iodevices import Ev3devSensor

class LSA(Ev3devSensor):

    def __init__(self, port):
        """Initialize the sensor."""

        # Initialize the parent class.
        super().__init__(port)

        # Get the sysfs path.
        self.path = '/sys/class/lego-sensor/sensor' + str(self.sensor_index)

    def get_commands(self):
        with open(self.path + '/commands', 'r') as m:

            # Read the contents.
            contents = m.read()

            # Strip the newline symbol, and split at every space symbol.
            return contents.strip().split(' ')


    def calibrate_white(self):
        # TODO
        pass

    def calibrate_black(self):
        # TODO
        pass

    def read_calibrated(self):
        return self.read('CAL')

    def read_raw(self):
        return self.read('RAW')
