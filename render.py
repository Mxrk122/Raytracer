from asyncio.windows_events import NULL
from operator import truediv
import writeutilities as wu


class Render(object):
    height = 1024
    width = 1024
    texture = None
    

    def __init__(self):
        ...

    # establecer el tamaño de nuestra imagen 
    def setSize(self, height, width):
        # self -> referencia a la propiedad de la clase
        self.height = height
        self.width = width
        self.vp_height = height
        self.vp_width = width

    # funcion para elegir el color del pincel
    def set_clear_color(self, r, g, b):

        self.clear_color = color.color_RGB_to_GBR(r, g, b)
    
    # funcion para elegir el color del pincel
    def set_color(self, r, g, b):
        red = int(r * 255)
        green = int(g * 255)
        blue = int(b * 255)

        self.vertex_color = color.color_RGB_to_GBR(red, green, blue)
    
    # funcion para elegir el color del pincel
    def set_clear_vp_color(self, r, g, b):
        red = int(r * 255)
        green = int(g * 255)
        blue = int(b * 255)

        self.clearvp_color = color.color_RGB_to_GBR(red, green, blue)

    # funcion para pintar todo el mapa de bits de un color
    def clear(self):
        self.framebuffer = [
            # for para rellenar el array -> generador
            # se pinta del color que indique clear_color
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

        self.z_framebuffer = [
            [-9999 for x in range(self.width)]
            for y in range(self.height)
        ]
    
    # funcion para elegir el color del pincel
    def set_vertex_color(self, r, g, b):
        self.vertex_color = color.color_RGB_to_GBR(r, g, b)
    
    # Funcion para pintar un punto en el viewport
    def simply_point(self, x, y):
        if x < 0 or y < 0: 
            return NULL
        try: 
            self.framebuffer[y][x] = self.vertex_color
        except:
            return
    
    # Funcion para pintar en el zbuffer
    def simply_z(self, x, y, z):

        if x < 0 or y < 0:
            return False

        if len(self.z_framebuffer[0]) <= x or len(self.z_framebuffer) <= y:
            return False
        
        if (self.z_framebuffer[y][x] < z):
            self.z_framebuffer[y][x] = z
            return True

    # Funcion para pintar una linea dadas las coordenadas
    def line_normal(self, x0, y0, x1, y1):

        x0 = int(x0)
        x1 = int(x1)
        y0 = int(y0)
        y1 = int(y1)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx

        if steep:
            # Si la linea tiende a ser mas vertical, cambiar coordenadas
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            # si la linea va hacia "atras", darle la vuelta a los puntos
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        threshold = dx

        y = y0
        for x in range(x0, x1):
            if steep:
                self.simply_point(y, x)
            else:
                self.simply_point(x, y)

            offset += dy * 2

            if offset >= threshold:
                # si la linea va hacia arriba, aumentar una unidad
                if y0 < y1:
                    y += 1
                else:
                # si la linea va hacia abajo, disminuir una unidad
                    y -= 1
                # Aumentar el threshold cada vez
                threshold += dx * 2
    
    #Funcion para definir una textura a nuestro siguiente objeto a dibujar
    def giveTexture(self, texture):
        
        self.texture = texture
    
    def triangle(self, vertex, object_color, tvertex=()):

        A, B, C = vertex

        if self.texture:
            tA, tB, tC = tvertex

        L = V3(0, 0, 1)
        N = cross_p((C - A), (B - A))
        i = L.normalize() @ N.normalize()

        if i < 0:
            i = abs(i)

        elif i > 1:
            i = 1
        
        #self.vertex_color = color.color_RGB_to_GBR(255 * i, 255 * i, 255 * i)
        self.vertex_color = color.color_RGB_to_GBR(
            object_color[0] * i,
            object_color[1] * i,
            object_color[2] * i
        )

        Bmin, Bmax = bounding_box(A, B, C)

        Bmin.round()
        Bmax.round()

    
        for x in range(Bmin.x, Bmax.x + 1):
            for y in range(Bmin.y, Bmax.y + 1):
                    w, u, v = barycentric(A, B, C, V2(x, y))

                    if (w < 0 or v < 0 or u < 0):
                        continue

                    z = A.z * w + B.z * v + C.z * u
                    

                    if(self.simply_z(x, y, z)):
                        
                        if self.texture:
                            
                            tX = tA.x * w + tB.x * v + tC.x * u
                            tY = tA.y * w + tB.y * v + tC.y * u
                            
                            self.vertex_color = self.texture.get_intensity(tX, tY, i)
                        
                        self.simply_point(x, y)


    # Metodo dedicado a escribir la informacion que especificamos
    # a lo largo de la creacion de la imagen
    def write(self, filename, width, height, framebuffer):
        file = open(filename, 'bw')

        """ Pixel Header -> debe ocupar 14 bytes """
        # Escribir b y m
        file.write(wu.char('B'))
        file.write(wu.char('M'))
        # tamaño del archivo
        file.write(wu.dword(14 + 40 + width * height * 3))
        # unknown
        file.write(wu.word(0))
        file.write(wu.word(0))
        # puntero del inicio
        file.write(wu.dword(14 + 40))

        """ info header -> 40 pixeles """
        file.write(wu.dword(40))
        file.write(wu.dword(width))
        file.write(wu.dword(height))
        file.write(wu.word(1))
        # RGB
        file.write(wu.word(24))
        file.write(wu.dword(0))
        file.write(wu.dword(width * height * 3))
        file.write(wu.dword(0))
        file.write(wu.dword(0))
        file.write(wu.dword(0))
        file.write(wu.dword(0))

        """ Pixel data -> la imagen en si """
        for y in range(height):
            for x in range(width):
                if type(framebuffer[y][x]) == type((0,0,0)):
                    file.write(b'3\x00\x00')
                else:
                    file.write(framebuffer[y][x])
        
        file.close()