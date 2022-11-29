import math
import plane
import random
from render import Render
from cube import cube
from triangle import triangle
import color
from vector3 import V3
from sphere import Sphere
from light import Light
from envmap import *

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, filename, width, height):
        self.filename = filename
        self.width = width
        self.height = height
        self.clear_color = (0, 0, 0)
        self.paint_color = (1, 1, 1)
        self.framebuffer = [[]]
        self.scene = []
        self.light = None
        self.bg: envmap = None
        self.clear()
    
    def setBackground(self, img_path):
        self.bg = envmap(img_path)
    
    def drawBackground(self, direction: V3):

        direction = direction.normalize()

        if self.bg:
            return self.bg.get_color(direction)
        else:
            return self.clear_color

    def change_paint_color(self, r, g, b):
        self.paint_color = (r, g, b)
    
    def change_clear_color(self, r, g, b):
        self.clear_color = (r, g, b)
    
    def set_light(self, position: V3, intensity, color):
        self.light = Light(position, intensity,  color)

    def point(self, x, y, c = None):
        if (y >= 0 and y < self.height) and (x >= 0 and x < self.width):
            if c != None:
                self.framebuffer[y][x] = color.color_RGB_to_GBR(*c)
            else:
                self.framebuffer[y][x] = color.color_RGB_to_GBR(*self.clear_color)

    # funcion para pintar todo el mapa de bits de un color
    def clear(self):
        self.framebuffer = [
            # for para rellenar el array -> generador
            # se pinta del color que indique clear_color
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self):
        r = Render()
        r.write(self.filename + ".bmp", self.width, self.height, self.framebuffer)

    def render(self):
        fov = int(math.pi/2)
        ar = self.width/self.height

        for y in range(self.height):
            for x in range(self.width):
                if 0 < random.random():
                    i = ((2 * (x + 0.5) / self.width) - 1) * math.tan(fov/2) * ar
                    j = ( 1 - (2 * (y + 0.5) / self.height)) * math.tan(fov/2) * ar

                    direction = V3(i, j, -1).normalize()
                    origin = V3(0, 0, 0)

                    c = self.cast_ray(origin, direction)

                    self.point(x, y, c)
        
    def addSphere(self, center: V3, radius, material):
        self.scene.append(Sphere(center, radius, material))
    
    def addPlane(self, center, w, l, material):
        hi = plane.Plane(center, w, l, material)
        self.scene.append(hi)

    def addCube(self, center, side, material):
        hi = cube(center, side, material)
        self.scene.append(hi)
    
    def addTriangle(self, vertices, material):
        hi = triangle(vertices, material)
        self.scene.append(hi)

    
    #Método para calcular la reflexión.
    def reflect(self, I, N):
        return (I - (N * 2 * (N @ I))).normalize()
    
    def retract(self, I, N, roi):
        etai = 1
        etat = roi

        cosi = (I @ N) * -1

        if (cosi < 0):
            cosi *= -1
            etai *= -1
            etat *= -1
            N *= -1
        
        eta = etai/etat

        k = 1 - eta ** 2 * (1 - cosi ** 2)

        if k < 0:
            return V3(0, 0, 0)
        
        cost = k ** 5

        return (I * eta) + (N * (eta * cosi - cost)).normalize()

    def scene_intersect(self, origin, direction):
        zBuffer = 999999

        material = None

        intersect = None

        for o in self.scene:
            obj_intersect = o.ray_intersect(origin, direction)
            
            if obj_intersect:
                if obj_intersect.distance < zBuffer:
                    zBuffer = obj_intersect.distance
                    material = o.material
                    intersect = obj_intersect
                    
        return material, intersect

    def cast_ray(self, origin, direction, recursion = 0):

        if recursion == MAX_RECURSION_DEPTH:
            return self.drawBackground(direction)

        material, intersect  = self.scene_intersect(origin, direction)

        if material == None:
            return self.drawBackground(direction)
        
        # direccion de la luz
        light_direction = (self.light.position - intersect.point).normalize()

        # Sombras
        shadow_bias = 1.1
        shadow_origin = intersect.point + (intersect.normal * shadow_bias)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_origin, light_direction)
        shadow_intensity = 0

        if shadow_material:
            # En la sombra
            shadow_intensity = 0.7

        # Diffuse component
        diffuse_intensity = light_direction @ intersect.normal

        diffuse = (
            material.diffuse[2] * diffuse_intensity * material.albedo[0] * (1 - shadow_intensity),
            material.diffuse[1] * diffuse_intensity * material.albedo[0] * (1 - shadow_intensity),
            material.diffuse[0] * diffuse_intensity * material.albedo[0] * (1 - shadow_intensity)
        )

        # Specular component
        light_reflection = self.reflect(light_direction, intersect.normal)
        reflection_intensity = max(0, light_reflection @ direction) 
        specular_intensity =  self.light.intensity * reflection_intensity ** material.spec

        specular = (
            self.light.color[2] * specular_intensity * material.albedo[1],
            self.light.color[1] * specular_intensity * material.albedo[1],
            self.light.color[0] * specular_intensity * material.albedo[1]
        )

        # reflection
        if material.albedo[2] > 0:
            reverse_direction = direction 
            reflect_direction = self.reflect(reverse_direction, intersect.normal)
            reflect_bias = -0.5 if reflect_direction @ intersect.normal < 0 else 0.5
            reflect_origin = intersect.point + (intersect.normal * reflect_bias) 
            reflect_color = self.cast_ray(reflect_origin, reflect_direction, recursion + 1)
        else:
            reflect_color = (0, 0, 0)
        
        reflection = (
            reflect_color[2] * material.albedo[2],
            reflect_color[1] * material.albedo[2],
            reflect_color[0] * material.albedo[2],
        )

        # refraction
        if material.albedo[3] > 0:
            refract_direction = self.retract(direction, intersect.normal, material.refractive_index)
            refract_bias = -0.5 if refract_direction @ intersect.normal < 0 else 0.5
            refract_origin = intersect.point + (intersect.normal * refract_bias) 
            refract_color = self.cast_ray(refract_origin, refract_direction, recursion + 1)
        else:
            refract_color = (0, 0, 0)
        
        refraction = (
            refract_color[2] * material.albedo[3],
            refract_color[1] * material.albedo[3],
            refract_color[0] * material.albedo[3]
        )

        result = (
            diffuse[2] + specular[2] + reflection[2] + refraction[2],
            diffuse[1] + specular[1] + reflection[1] + refraction[1],
            diffuse[0] + specular[0] + reflection[0] + refraction[0]
        )

        return result