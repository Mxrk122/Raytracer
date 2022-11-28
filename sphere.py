from sympy import false
from intersect import *

class Sphere(object):
    def __init__(self, center, radius, material) -> None:
        self.center = center
        self.radius = radius
        self.material = material
    
    def ray_intersect(self, origin, direction):
        L = self.center - origin
        tca = L @ direction
        l = L.length()

        d2 = l**2 - tca**2

        if d2 > self.radius**2:
            return None
        
        thc = (self.radius**2 - d2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        impact_point = direction *  t0 + origin
        normal = (impact_point - self.center)
        

        return intersect(
            distance = t0,
            point = impact_point,
            normal = normal.normalize() 
        )