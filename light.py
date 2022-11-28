from vector3 import V3
class Light(object):
    def __init__(self, position: V3, intensity, color):
      self.position = position
      self.intensity = intensity
      self.color = color