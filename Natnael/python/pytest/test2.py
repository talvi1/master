import serial

ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3000, bytesize=8, parity='N')

try:
    ser.isOpen();
    print("Serial port is open")

except:
    print("Error")

if(ser.isOpen()):
    try:
        while(1):
            print(ser.readline())
    except Exception:
         print("error1")
else:
    print("Cannot print  serail port")
