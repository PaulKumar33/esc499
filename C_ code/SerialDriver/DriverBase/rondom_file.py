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

ser = serial.Serial('COM3', 115200)
rl = ReadLine(ser)
ar = []
samps = 0
import time

cur = time.time()
while(samps < 10):
    ar.append(rl.readline())
    samps = time.time()-cur

print(len(ar))