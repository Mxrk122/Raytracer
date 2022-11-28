class Material(object):
    def __init__(self, diffuse, albedo, spec, refractive_index = 0) -> None:
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec
        self.refractive_index = refractive_index