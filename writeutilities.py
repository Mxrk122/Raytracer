# Archivo dedicado a convertir bits a los bytes que necesitamos
import struct

def char(c):
    # unidad de 1 byte
    # esta funcion convierte el character a su representacion en bytes con un encoding
    # se convierten los bits del caracter a un byte 
    encoded = c.encode('ascii')
    value = struct.pack('=c', encoded)
    return value    

def word(w):
    # ocupa 2 bytes
    # utilizarlo para numeros principalmente
    value = struct.pack('=h', w)
    return value

def dword(d):
    # escribe 4 bytes
    value = struct.pack('=l', d)
    return value
