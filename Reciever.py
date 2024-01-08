import serial

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

ser = serial.Serial('COM6', 9600)
ser.write(b"he\n")
rl = ReadLine(ser)

def read():
    data = None
    while ser.in_waiting > 4:    
        data = rl.readline()
    if data == None:
        return None
    if len(data) != 4:
        return None
    x,y,z,_ = data
    return (x,y,z)

