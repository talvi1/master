import time
import serial
from time import sleep
import spidev


bus = 0

device = 0

spi = spidev.SpiDev()

spi.open(bus, device)

sleep(0.33)
spi.max_speed_hz = 500000
spi.mode = 0
to_send = [0x7E, 0x00, 0x04, 0x08, 0x01, 0x48, 0x56, 0x58]
response  = spi.xfer2(to_send)
hex_array = [hex(x) for x in response]
print(hex_array)
spi.close()


#ser= serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=8, parity='N', stopbits=1)

#to_send = [0x7E, 0x00, 0x0A, 0x01, 0x01, 0x00, 0x02, 0x00, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x07]
#ser.write(serial.to_bytes(to_send))
#ser.write(serial.to_bytes([0x7E, 0x00, 0x0A, 0x01, 0x01, 0x00, 0x02, 0x00, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x07]))

#while True:
 #   data = ser.read()
 #   print(hex(ord(data)))