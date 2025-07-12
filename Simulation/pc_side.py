import serial

pc = serial.Serial(port='/dev/pts/2', baudrate=9600, timeout=0.1)
while True:
    msg_to_Ar = input("Send to Arduino: ")
    pc.write((msg_to_Ar + '\n').encode('utf-8'))  

    read_from_Ar = pc.readline().decode('utf-8').strip()
    print("\nReceived from Arduino:", read_from_Ar)
