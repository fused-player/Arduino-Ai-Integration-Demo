import serial
def task(to_do):
    #DO SOME ARDUINO STUFF
    if to_do == "light_on":
        print("LED LIGHTS TURNED ON : ENJOY")
    elif to_do == "light_off":
        print("LED LIGHTS TURNED OFF : ENJOY")
        
def servo(to_do):
    new = to_do.split("_")
    if (new[0] == "servo"):
        degrees = new[2]
        print(f"\nServo rotated by {degrees} degrees")
arduino = serial.Serial(port='/dev/pts/6', baudrate=9600, timeout=0.1)

while True:  # Keep checking for messages
    if arduino.in_waiting > 0:
        received_msg = arduino.readline().decode('utf-8').strip()
        task(received_msg)
        servo(received_msg)
        print("Received from PC:", received_msg)
        
        arduino.write((received_msg + 'TASK_DONE\n').encode('utf-8'))
