import ray
from vector3 import V3
from material import *
import color

filename = "base"
r = ray.Raytracer(filename, 600, 600)
r.change_clear_color(0.2, 0.8, 1)

r.clear()


rubber = Material(diffuse=(180/255, 0, 0), albedo = [0.9, 0.1, 0, 0], spec = 10)

mirror = Material(diffuse=(1, 1, 1), albedo = [0, 1, 0.8, 0], spec = 142)

nosexd = Material(diffuse=(1, 1, 1), albedo = [0.2, 0.8, 0], spec = 10)

glass = Material(diffuse=(150/255, 180/255, 200/255), albedo = [0, 0.5, 0.1, 0.8], spec = 125, refractive_index=1.5)

# reflexión
water = Material((0.8, 0.8, 1), [0, 0.5, 0.1, 0.8], 10, 1.5)
white_block = Material(diffuse=(1, 1, 0.8), albedo = [0.6, 0.3, 0, 0], spec = 50)
orange_block = Material(diffuse=(1, 0.4, 0.1), albedo = [0.6, 0.3, 0, 0], spec = 50)
black_block = Material(diffuse=(0, 0, 0.4), albedo = [0.6, 0.3, 0, 0], spec = 50)
grass = black_block = Material(diffuse=(0.8, 1, 0.4), albedo = [0.6, 0.3, 0, 0], spec = 50)

#r.setBackground('./hola.bmp')
# change the light
r.set_light(V3(0, -5, -5), 20, (0, 0, 0))



#result
r.addCube(V3(-2.5, 2, -3), 3.5, white_block)
r.addCube(V3(2.5, 2, -3), 3.5, white_block)
r.addPlane(V3(0, -0.5, -3), 3, 15, water)

r.addCube(V3(-2.6, 1.9, -3), 3.5, grass)
r.addCube(V3(2.6, 1.9, -3), 3.5, grass)


#base
r.addCube(V3(0, 0.5, -13), 2, white_block)
r.addCube(V3(2, 0.5, -13), 2, white_block)
r.addCube(V3(4, 0.5, -13), 2, white_block)
r.addCube(V3(-2, 0.5, -13), 2, white_block)
r.addCube(V3(-4, 0.5, -13), 2, white_block)

r.addCube(V3(0, 1.1, -12), 2, orange_block)
r.addCube(V3(2, 1.1, -12), 2, orange_block)
r.addCube(V3(4, 1.1, -12), 2, orange_block)
r.addCube(V3(-2, 1.1, -12), 2, orange_block)
r.addCube(V3(-4, 1.1, -12), 2, orange_block)

#building
r.addCube(V3(0, -4, -28), 9, white_block)
r.addCube(V3(4, -3, -30), 9, white_block)
r.addCube(V3(-4, -3, -30), 9, white_block)

r.addSphere(V3(0, -7, -28), 5.5, white_block)
r.addSphere(V3(5, -7, -29), 4, white_block)
r.addSphere(V3(-5, -7, -29), 4, white_block)

r.addTriangle(((0.5, -4.5, -10), (-0.5, -4.5, -10), (0, -5.5, -10)), black_block)

print("renderizando")
r.render()
r.write()