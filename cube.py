class Cube:
    def __init__(self, id, neighborCubes, isEnergyCenter):
        self.id = id
        self.neighborCubes = neighborCubes
        self.isEnergyCenter = isEnergyCenter


class CubeSideInfo:
    def __init__(self, attachedCubeId, cubeSide):
        self._attachedCubeId = attachedCubeId
        self._cubeSide = cubeSide
