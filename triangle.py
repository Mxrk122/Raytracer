from intersect import *
from vector3 import *
# Definición de la clase Triangle.
# basado en Scratchapixel
class triangle(object):

  
  def __init__(self, vertices, material):
    self.vertices = vertices
    self.material = material

  
  def ray_intersect(self, origin, direction):

    #los vertices vienen en vector3
    v1 = V3(*self.vertices[0])
    v2 = V3(*self.vertices[1])
    v3 = V3(*self.vertices[2])

    # calcular el perimetro y cantidades del área desde el origen -> v1
    f_line = (v2 - v1)
    s_line = (v3 - v1)
    h = direction * s_line
    q = ((origin - v1) * f_line)
    
    # si la inlcinacion es 0 no hay rayo
    inc = f_line @ h
    i_inc = inc
    if -1E-06 < inc < 1E-06:
      return None
    i_inc = 1 / i_inc

    # u representa otra inclinacion
    u = i_inc * ((origin - v1) @ h)
    if (u < 0) or (u > 1):
      return None

    #vertice -> no dibujar si se sale del eprimetro en abse al vertice
    v = i_inc * (direction @ q)
    if ((v < 0) or ((u + v) > 1)):
      return None

    t = i_inc * (s_line @ q)
    if (t > 1E-06):
      # si estamos dentro del area -> dibujar.
      impact = origin + (direction * t)
      normal = (f_line * s_line).normalize()
      return intersect(t, impact, normal,)
    else:
      return None