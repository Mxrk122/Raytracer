from vector3 import *
from intersect import *

class cube(object): 
    def __init__(self, center: V3, lats, material) -> None:
        self.side = lats
        self.center = center
        self.material = material

    def ray_intersect(self, orig, direction):
        tmin = -99999
        tmax = 99999

        for i in range(3):
            current_direction = abs(direction.getValuesTuple()[i])

            center_direction = self.center.getValuesTuple()[i] - self.side / 2

            center_c_direction = self.center.getValuesTuple()[i] + self.side / 2

            if current_direction < 1e-6:
                if orig.getValuesTuple()[i] < center_direction or orig.getValuesTuple()[i] > center_c_direction:
                    return None
            else:
                t1 = (center_direction - orig.getValuesTuple()[i]) / direction.getValuesTuple()[i]
                t2 = (center_c_direction - orig.getValuesTuple()[i]) / direction.getValuesTuple()[i]

                # en caasod e que los rayos sobrepsaen invertirlos
                if t1 > t2:
                    new_t2 = t1
                    new_t1 = t2

                    t1 = new_t1
                    t2 = new_t2

                if t1 > tmin:
                    tmin = t1

                if t2 < tmax: 
                    tmax = t2

                if tmin > tmax:
                    return None

        if tmin < 0:
            tmin = tmax

            if tmin < 0:
                return None

        impact = orig + (direction * tmin)
        normal = (impact - self.center).normalize()

        return intersect(tmin, impact, normal)