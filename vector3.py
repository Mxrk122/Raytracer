from array import array


class V3(object):

    def __init__(self, x, y = 0, z = 0, w = 0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
    def __add__(self, other):
        return V3((self.x + other.x), (self.y + other.y), (self.z + other.z))
    
    def __sub__(self, other):
        if type(other) == V3:
            return V3((self.x - other.x), (self.y - other.y), (self.z - other.z))
        else:
            return V3(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if ((type(other) == int) or (type(other) == float)):
            return V3((other * self.x), (other * self.y), (other * self.z))
        else:
            return V3(
                ((self.y * other.z) - (self.z * other.y)),
                ((self.z * other.x) - (self.x * other.z)),
                ((self.x * other.y) - (self.y * other.x))
            )

    def __matmul__(self, other):
        return ((self.x * other.x) + (self.y * other.y) + (self.z * other.z))

    def __len__(self):
        return (((self.x ** 2) + (self.y ** 2) + (self.z ** 2)) ** 0.5)
    
    def normalize(self):
        try:
            return (self * (1 / self.__len__()))
        except:
            return (self * 0)

    def __repr__(self):
        return f"<{self.x}, {self.y}, {self.z}>"
    
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)

    def matrixToVector(self, matrix):
        self.x, self.y, self.z, self.w = matrix

    def getValues(self):
        return self.x, self.y, self.z
    
    def getValuesTuple(self):
        return (self.x, self.y, self.z)
    
    def cross_p(self, other):
        return V3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
