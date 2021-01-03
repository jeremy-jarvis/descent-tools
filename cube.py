from enum import Enum

class CubeSide(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    BACK = 4
    FRONT = 5

class VertexPosition(Enum):
    LEFT_FRONT_TOP = 0
    LEFT_FRONT_BOTTOM = 1
    RIGHT_FRONT_BOTTOM = 2
    RIGHT_FRONT_TOP = 3
    LEFT_BACK_TOP = 4
    LEFT_BACK_BOTTOM = 5
    RIGHT_BACK_BOTTOM = 6
    RIGHT_BACK_TOP = 7

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


