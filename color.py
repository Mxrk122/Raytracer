def color_RGB_to_GBR(r, g, b):

    r = r * 255
    if r >= 254:
        r = 254
    
    if r <= 0:
        r = 0

    g = g * 255
    if g >= 254:
        g = 254
    
    if g < 0:
        g = 0

    b = b * 255
    if b >= 254:
        b = 254
    
    if b < 0:
        b = 0

    #retornar en bytes
    return bytes([int(b), int(g), int(r)])