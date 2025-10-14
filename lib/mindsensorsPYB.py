#!/usr/bin/env pybricks-micropython
from pybricks.iodevices import I2CDevice

## mindsensors_i2c: this class provides i2c functions
#  for read and write operations.
class mindsensors_i2c():
    
    def __init__(self,port, i2c_address):
        self.port = port
        self.i2c_address=i2c_address
        self.i2c = I2CDevice(port,i2c_address>>1)


    def errMsg(self):
        print ("Error accessing 0x%02X: Check your I2C address" % self.address)
        return -1

    ## Read a string from your i2c device starting at a given location
    #  @param self The object pointer.
    #  @param reg The first register of the string to read from.
    #  @param length The length of the string.
    def readString(self, reg, length):
        return self.i2c.read(reg, length)


    ## Read an unsigned byte from your i2c device at a given location
    #  @param self The object pointer.
    #  @param reg The register to read from.
    def readByte(self, reg):
        a = self.i2c.read(reg, 1)
        return int.from_bytes(a, "little")

    ## Write a byte to your i2c device at a given location
    #  @param self The object pointer.
    #  @param reg The register to write value at.
    #  @param value Value to write.
    def writeByte(self, reg, value):
        self.i2c.write( reg,value)
        pass

    ## Write a command to your i2c device at a command location
    #  @param self The object pointer.
    #  @param comamnd to write .
    def issueCommand(self,  value):
        self.i2c.write( 0x41, value)
        
    ## Read a byte array from your i2c device starting at a given location
    #  @param self The object pointer.
    #  @param reg The first register in the array to read from.
    #  @param length The length of the array.
    def readArray(self, reg, length):

        return self.i2c.read(reg, length)
        
    ## Write a byte array from your i2c device starting at a given location
    #  @param self The object pointer.
    #  @param reg The first register in the array to write to.
    #  @param arr The array to write.
    def writeArray(self, reg, arr):
        return self.i2c.write(reg, bytearray(arr))
        
    ## Read a signed byte from your i2c device at a given location
    #  @param self The object pointer.
    #  @param reg The register to read from.
    def readByteSigned(self, reg):
        a = self.i2c.read(reg, 1)
        signed_a =int.from_bytes(a, "little") #ctypes.c_byte.value 
        return signed_a

    ## Write an unsigned 16 bit integer from your i2c device from a given location. little endian write integers.
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to write.
    #  @param int The integer to write.
    def writeInteger(self, reg, i):        
        i = int(i)
        results = self.i2c.write(reg, [i%256, (i>>8)%256])

    ## Read a signed 16 bit integer from your i2c device from a given location. Big endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readIntegerSignedBE(self, reg):
        a = self.readIntegerBE(reg)
        if a&0x8000 : a = a -65535 
        return a       
    
    ## Read a signed 16 bit integer from your i2c device from a given location. little endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readIntegerSigned(self, reg):
        a = self.readInteger(reg)
        if a&0x8000 : a = a -65535 
        return a

    ## Read an unsigned 32bit integer from your i2c device from a given location. Big endian read integers.
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readLongBE(self, reg):
        
        results = self.i2c.read(reg,4)
        return results[3] + (results[2]<<8)+(results[1]<<16)+(results[0]<<24)           
        
    ## Read an unsigned 32bit integer from your i2c device from a given location. little endian read integers.
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readLong(self, reg):
        results = self.i2c.read(reg,4)
        return results[0] + (results[1]<<8)+(results[2]<<16)+(results[3]<<24)       

    ## Read a signed 32bit integer from your i2c device from a given location. Big endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readLongSignedBE(self, reg):
        a = self.readLongBE(reg)
        if a&0x80000000 : a = a -0xFFFFFFFF
        return a    

    ## Read a signed 32bit integer from your i2c device from a given location. little endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readLongSigned(self, reg):
        a = self.readLong(reg)
        if a&0x80000000 : a = a -0xFFFFFFFF
        return a

    ##  Read the firmware version of the i2c device
    #  @param self The object pointer.
    def GetFirmwareVersion(self):
        try:
            ver = self.readString(0x00, 8)
            return ver
        except:
            print( "Error: Could not retrieve Firmware Version" )
            print ("Check I2C address and device connection to resolve issue")
            return ""

    ## Read an unsigned 16 bit integer from your i2c device from a given location.  Big-endian read integers .
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readIntegerBE(self, reg):        
        results = self.i2c.read( reg, 2)
        return results[1] + (results[0]<<8)
        
    ## Read an unsigned 16 bit integer from your i2c device from a given location. little endian read integers.
    #  @param self The object pointer.
    #  @param reg The first register of the first byte of the integer to read.
    def readInteger(self, reg):        
        try:
            results = self.i2c.read(reg, 2)
            return results[0] + (results[1]<<8)
        except:
            return 0    

    ##  Read the vendor name of the i2c device
    #  @param self The object pointer.
    def GetVendorName(self):
        try:
            vendor = self.readString(0x08, 8)
            return vendor
        except:
            print ("Error: Could not retrieve Vendor Name")
            print ("Check I2C address and device connection to resolve issue")
            return ""
            
    ##  Read the i2c device id
    #  @param self The object pointer.
    def GetDeviceId(self):
        try:    
            device = self.readString(0x10, 8)
            return device
        except:
            print ("Error: Could not retrieve Device ID")
            print ("Check I2C address and device connection to resolve issue")
            return ""

## LSA: this class provides functions for LightSensorArray from mindsensors.com
#  for read and write operations.
class LSA(mindsensors_i2c):
    LSA_ADDRESS = const(0x14)

    LSA_COMMAND = const(0x41)
    
    LSA_CALIBRATED = const(0x42)

    LSA_UNCALIBRATED = const(0x6A)

    LSA_WHITE_LIMIT = const(0x4A)

    LSA_BLACK_LIMIT = const(0x52)

    LSA_WHITE_CALIBRATION_DATA = const(0x5A)

    LSA_BLACK_CALIBRATION_DATA = const(0x62)

    ## Initialize the class with the i2c address of your LightSensorArray
    #  @param self The object pointer.
    #  @param lsa_address Address of your LightSensorArray.
    def __init__(self, port):
        mindsensors_i2c.__init__(self, port, self.LSA_ADDRESS)
        self.wakeup()

    ## Writes a value to the command register
    #  @param self The object pointer.
    #  @param cmd Value to write to the command register.
    def write_command(self, cmd):
        self.i2c.write(reg=self.LSA_COMMAND, data=cmd)

    def read_current_command(self):
        return self.readByte(reg=self.LSA_COMMAND)

    ## Calibrates the white value for the LightSensorArray
    #  @param self The object pointer.
    def calibrate_white(self):
        self.write_command(b'W')

    ## Calibrates the black value for the LightSensorArray
    #  @param self The object pointer.
    def calibrate_black(self):
        self.write_command(b'B')

    ## Wakes up or turns on the LEDs of the LightSensorArray
    #  @param self The object pointer.
    def wakeup(self):
        self.write_command(b'P')

    ## Puts to sleep, or turns off the LEDs of the LightSensorArray
    #  @param self The object pointer.
    def sleep(self):
        self.write_command(b'D')

    def get_data(self, address, size):
        try:
            data = self.i2c.read(address, size)
            
            if data != None:
                out = []

                for d in data:
                    out.append(int(d))
                return out
            else:
                print("WARNING: no data has returned")
        except OSError as err:
            print("ERROR: i2c device is not responding, check the wiring")

    ## Reads the eight(8) calibrated light sensor values of the LightSensorArray
    #  @param self The object pointer.
    def read_calibrated(self) -> list:
        b = self.get_data(self.LSA_CALIBRATED, 8)
        return b

    ## Reads the eight(8) uncalibrated light sensor values of the LightSensorArray
    #  @param self The object pointer.
    def read_raw_voltages(self):
        s = self.get_data(self.LSA_UNCALIBRATED, 16)
        array = [s[0:1], s[2:3], s[4:5], s[6:7], s[8:9], s[10:11], s[12:13], s[14:15] ]
        return array

    def get_white_limit(self):
        data = self.get_data(self.LSA_WHITE_LIMIT, 8)
        arr = [ data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7] ]
        return arr

    def get_black_limit(self):
        data = self.get_data(self.LSA_BLACK_LIMIT, 8)
        arr = [ data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7] ]
        return arr

    def get_white_calibration_data(self):
        data = self.get_data(self.LSA_WHITE_CALIBRATION_DATA, 8)
        arr = [ data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7] ]
        return arr

    def get_black_calibration_data(self):
        data = self.get_data(self.LSA_BLACK_CALIBRATION_DATA, 8)
        arr = [ data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7] ]
        return arr
