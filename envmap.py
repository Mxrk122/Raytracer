import struct
from math import *
class envmap(object):
    def __init__(self, path):
        self.path = path
        self.width = 1000
        self.height = 1000
        self.pixels = []
        self.read()
    
    def read(self):
        with open(self.path, "rb") as envmap:
            envmap.seek(2 + 4 + 4) 
            header_size = struct.unpack("=l", envmap.read(4))[0] 
            envmap.seek(2 + 4 + 4 + 4 + 4)
            # Encontrar el width  height
            self.width = struct.unpack("=l", envmap.read(4))[0]
            self.height = struct.unpack("=l", envmap.read(4))[0]
            envmap.seek(header_size)

            for y in range(self.height):
                self.pixels.append([])
                for line in range(self.width):
                    b, g, r = ord(envmap.read(1)), ord(envmap.read(1)), ord(envmap.read(1))


                    self.pixels[y].append((r, g, b)) 


    def get_color(self, direction):
        direction = direction.normalize()

        # controlar casos que se salen de la imagen
        x = round(((atan2(direction.z, direction.x) / (2 * pi)) + 0.5) * self.width)
        x -= 1 if (x > 0) else 0

        y = (-1 * round((acos((-1 * direction.y)) / pi) * self.height))
        y -= 1 if (y > 0) else 0

        return self.pixels[y][x]