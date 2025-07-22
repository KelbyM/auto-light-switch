import smbus2

class BH1750:
    """
    Manages the BH1750 sensor that is connected to the Raspberry Pi.
    """
    ADDRESS = 0x23 
    POWER_ON = 0x01
    RESET = 0x07
    CONT_HI_RES = 0x10

    def __init__(self):
        self.bus = smbus2.SMBus(1)
        self._activate()
        
    def _activate(self):
        """
        Activates the BH1750 and sets it to continuous high-res mode.
        """
        self.bus.write_byte(self.ADDRESS, self.POWER_ON) # power on
        self.bus.write_byte(self.ADDRESS, self.RESET) # reset
        self.bus.write_byte(self.ADDRESS, self.CONT_HI_RES) # continuous high-res mode
        
    def get_lux(self) -> float:
        """
        Gets data from the BH1750, then calculates and returns the lux value.

        Returns:
            float: The lux value.
        """
        data = self.bus.read_i2c_block_data(self.ADDRESS, self.CONT_HI_RES, 2)
        lux = ((data[0] << 8) + data[1]) / 1.2
        return lux
