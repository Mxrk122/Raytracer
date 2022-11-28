import ray
from vector3 import V3
from material import *
import color

filename = "result"
r = ray.Raytracer(filename, 1920, 1080)
r.change_clear_color(0, 0, 0.2)

r.clear()

ivory = Material(diffuse=(200/255, 200/255, 180/255), albedo = [0.6, 0.3, 0, 0], spec = 50)
rubber = Material(diffuse=(180/255, 0, 0), albedo = [0.9, 0.1, 0, 0], spec = 10)

mirror = Material(diffuse=(1, 1, 1), albedo = [0, 1, 0.8, 0], spec = 142)

nosexd = Material(diffuse=(1, 1, 1), albedo = [0.2, 0.8, 0], spec = 10)

glass = Material(diffuse=(150/255, 180/255, 200/255), albedo = [0, 0.5, 0.1, 0.8], spec = 125, refractive_index=1.5)

r.setBackground('./hola.bmp')
# change the light
r.set_light(V3(-20, 20, 20), 2, (0, 0, 0))

#oso 1
#cuerpo
r.addTriangle(((-1, -2, -7.5), (-2, -2, -7.5), (-1.5, -3, -7.5)), ivory)




#r.addSphere(V3(-2, 1, -10), 2, mirror)

print("renderizando")
r.render()
r.write()