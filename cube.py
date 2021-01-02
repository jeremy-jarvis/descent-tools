from enum import Enum

class CubeSide(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    BACK = 4
    FRONT = 5

class NeighborCubeInfo:
    def __init__(self, attachedCubeId, cubeSide):
        self._attachedCubeId = attachedCubeId
        self._cubeSide = cubeSide

class EnergyCenterInfo:
    def __init__(self, special, energyCenterNumber, value):
        self.special = special
        self.energyCenterNumber = energyCenterNumber
        self.value = value

class WallInfo:
    def __init__(self, wallId, cubeSide):
        self.wallId = wallId
        self.cubeSide = cubeSide

class TextureInfo:
    def __init__(self, primaryTextureId, secondaryTextureId, cubeSide):
        self.primaryTextureId = primaryTextureId
        self.secondaryTextureId = secondaryTextureId
        self.cubeSide = cubeSide

class Cube:
    def __init__(self, id, neighborCubes, isEnergyCenter, vertexIndices, energyCenterInfo, staticLightFP, wallInfoList, textureInfoList):
        self.id = id
        self.neighborCubes = neighborCubes
        self.isEnergyCenter = isEnergyCenter
        self.vertexIndices = vertexIndices
        self.energyCenterInfo = energyCenterInfo
        self.staticLightFP = staticLightFP
        self.wallInfoList = wallInfoList
        self.textureInfoList = textureInfoList


