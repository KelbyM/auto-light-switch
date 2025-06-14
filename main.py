import smbus2
import time

DEVICE = 0x23
bus = smbus2.SMBus(1)

bus.write_byte(DEVICE, 0x01) # power on
bus.write_byte(DEVICE, 0x07) # reset
bus.write_byte(DEVICE, 0x10) # continuous high-res mode

while(1):
	time.sleep(1)
	data = bus.read_i2c_block_data(DEVICE, 0x10,2) # getting the data from the sensor
	lux = ((data[0] << 8) + data[1]) / 1.2 # calculating the lux value
	print(f"light level: {lux:.2f} lux") # printing the lux value
