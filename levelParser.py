import io
import sys
import binascii
from bitstring import BitArray
from fixedpoint import FixedPoint

from cube import NeighborCubeInfo, Cube, CubeSide, EnergyCenterInfo, WallInfo, TextureInfo, VertexPosition

def convert_coord_bytes_to_decimal(coordBytes):
    # Print Info about bytes
    print("coordBytes: " + str(coordBytes))
    coordBytes.reverse() # Reverses byte order, to account for little endianess
    print("coordBytes after reverse: " + str(coordBytes))
    
    coordBytesHex = "0x" + coordBytes.hex()
    print("coordBytesHex: " + coordBytesHex)
    
    coordBitArray = BitArray(hex=coordBytes.hex())
    print("coordBitArray: " + coordBitArray.bin)
    print("Length of coordBitArray: " + str(len(coordBitArray.bin)))

    bitString = "0b" + coordBitArray.bin
    print("bitString: " + bitString)
    
    # Create fixed point number
    coordFP = FixedPoint(bitString, signed=1, m=16, n=16, str_base=2)
    print("coordFP: " + str(coordFP))
    
    # Print out with decimal in correct location
    a = coordFP
    print(f"{a:#0{a.m+2}bm}.{a:0{a.n}bn}")
    print("coordFP fixed-point float: " + str(float(coordFP)))
    
    # Print info about fixed-point number
    print("Q-Format: " + coordFP.qformat)
    
    return coordFP


############ Beginning of script ###############

numberOfArguments = len(sys.argv)
if(numberOfArguments < 2):
    print("Error: No level file name (*.rdl) provided.")
    sys.exit()

levelFileName = str(sys.argv[1])

if(numberOfArguments == 3):
    outputFileName = str(sys.argv[2])
else:
    outputFileName = None

with open(levelFileName, "rb") as level_file:
    dataBytes = level_file.read()

data = io.BytesIO(dataBytes)

# Parse the header

signature = data.read(4)
print("Signature: " + str(signature, "utf8"))

versionBytes = data.read(4)
version = int.from_bytes(versionBytes, "little")
print("Version: " + str(version))

mineDataOffsetBytes = data.read(4)
mineDataOffset = int.from_bytes(mineDataOffsetBytes, "little")
print("Mine data offset: " + str(mineDataOffset))

objectsOffsetBytes = data.read(4)
objectsOffset = int.from_bytes(objectsOffsetBytes, "little")
print("Objects offset: " + str(objectsOffset))

fileSizeBytes = data.read(4)
fileSize = int.from_bytes(fileSizeBytes, "little")
print("File size: " + str(fileSize))

# Parse the Mine Structures

spacer = data.read(1)

# Parse Vertices

vertexCountBytes = data.read(2)
# print("Vertex count bytes: " + str(vertexCountBytes.hex()))
vertexCount = int.from_bytes(vertexCountBytes, "little")
print("Vertex count: " + str(vertexCount))

cubeCountBytes = data.read(2)
# print("Cube count bytes: " + str(cubeCountBytes.hex()))
cubeCount = int.from_bytes(cubeCountBytes, "little")
print("Cube count: " + str(cubeCount))

verticesBytes = data.read(vertexCount * 12) # 12 bytes per vertex
vertices = io.BytesIO(verticesBytes)
vertexCoords = []
cubes = []

for index in list(range(vertexCount)):
    print("=========== VERTEX =============")
    vertexBytes = vertices.read(12)
    vertex = bytearray(vertexBytes)
    print("Length of vertex bytearray: " + str(len(vertex)))
    vertexBits = BitArray(hex=vertex.hex())
    print("vertexBits: " + vertexBits.bin)

    # xBytesOriginal = vertex[0:4]
    # xBits = BitArray(hex=xBytesOriginal.hex())
    # print("Original X Bits: " + xBits.bin)
    # print("Original X Bits in Byte form: " + str(xBits.bytes))
    # yBytesOriginal = vertex[4:8]
    # yBits = BitArray(hex=yBytesOriginal.hex())
    # print("Original Y Bits: " + yBits.bin)
    # print("Original Y Bits in Byte form: " + str(yBits.bytes))
    # zBytesOriginal = vertex[8:12]
    # zBits = BitArray(hex=zBytesOriginal.hex())
    # print("Original Z Bits: " + zBits.bin)
    # print("Original Z Bits in Byte form: " + str(zBits.bytes))

    xBytes = vertex[0:4]
    yBytes = vertex[4:8]
    zBytes = vertex[8:12]

    print("\n")
    print("=========== Calculating X ============")
    x = convert_coord_bytes_to_decimal(xBytes)
    print("\n")
    print("=========== Calculating Y ============")
    y = convert_coord_bytes_to_decimal(yBytes)
    print("\n")
    print("=========== Calculating Z ============")
    z = convert_coord_bytes_to_decimal(zBytes)

    print("\n")
    print("======== Coordinate: " + str(float(x)) + ", " + str(float(y)) + ", " + str(float(z)))
    print("\n")

    vertexCoords.append([x, y, z])

for vertex in vertexCoords:
    print(str(float(vertex[0])) + "  " + str(float(vertex[1])) + "  " + str(float(vertex[2])))

print("\nVertices Parsed: " + str(len(vertexCoords)) + "\n")

# Parse cubes
numberOfSidesOnACube = 6
bytesPerCubeId = 2
cubeId = 0 # Does this start at zero or one?

for cubeIndex in list(range(cubeCount)):
    # Get CubeNeighborBitmask
    cubeNeighborBitmaskBytes = data.read(1)
    print("cubeNeighborBitmaskBytes: " + str(cubeNeighborBitmaskBytes.hex()))
    cubeNeighborBitmaskArray = BitArray(hex=cubeNeighborBitmaskBytes.hex())
    cubeNeighborBitmaskArray.reverse()
    print("Cube neighbor bitmask: " + cubeNeighborBitmaskArray.bin)

    # Count number of attached cubes
    numberOfAttachedCubes = 0
    for index in list(range(numberOfSidesOnACube)):
        if(cubeNeighborBitmaskArray[index] == 1):
            numberOfAttachedCubes+=1

    print("Number of neighbor cubes: " + str(numberOfAttachedCubes))

    # Get neighbor cube Ids
    numBytesForNeighborCubeIds = numberOfAttachedCubes * bytesPerCubeId
    neighborCubeIdsBytes = data.read(numBytesForNeighborCubeIds)
    neighborCubeIds = io.BytesIO(neighborCubeIdsBytes)

    # Gather side and cube Id for each neighbor cube
    neighborCubes = []
    for index in list(range(numberOfSidesOnACube)):
        print("========== index: " + str(index) + " ==================")
        bit = cubeNeighborBitmaskArray[index]
        if(bit == 1):
            attachedCubeIdBytes = neighborCubeIds.read(2)
            attachedCubeId = int.from_bytes(attachedCubeIdBytes, "little")
            neighborCubes.append(NeighborCubeInfo(attachedCubeId, index))

    # Get vertex references
    numberOfVertexReferences = 8
    vertexReferenceByteSize = 2
    vertexIndices = []
    print("Number of Vertex Indices: " + str(numberOfVertexReferences))
    for index in list(range(numberOfVertexReferences)):
        vertexIndexBytes = data.read(vertexReferenceByteSize)
        vertexIndex = int.from_bytes(vertexIndexBytes, "little")
        vertexIndices.append(vertexIndex)

    isEnergyCenter = cubeNeighborBitmaskArray[6] == 1
    print("isEnergyCenter: " + str(isEnergyCenter))

    energyCenterInfo = None

    if(isEnergyCenter):
        specialByte = data.read(1)
        special = int.from_bytes(specialByte, "little")
        energyCenterNumberByte = data.read(1)
        energyCenterNumber = int.from_bytes(energyCenterNumberByte, "little")
        valueBytes = data.read(2)
        value = int.from_bytes(valueBytes, "little")
        energyCenterInfo = EnergyCenterInfo(special, energyCenterNumber, value)

    # Get static light value. It is a fixed-point number in Q4.12 format.
    staticLightBytes = data.read(2)
    staticLightByteArray = bytearray(staticLightBytes)
    staticLightByteArray.reverse()
    staticLightBitArray = BitArray(hex=staticLightByteArray.hex())
    staticLightBitString = "0b" + staticLightBitArray.bin
    print("static light bitString: " + staticLightBitString)
    staticLightFP = FixedPoint(staticLightBitString, signed=0, m=4, n=12, str_base=2)
    print("static light fixed-point: " + str(staticLightFP))
    a = staticLightFP
    print(f"{a:#0{a.m+2}bm}.{a:0{a.n}bn}")
    print("static light fixed-point float: " + str(float(staticLightFP)))

    # Get info about walls
    walls = []
    wallsBitmaskBytes = data.read(1)
    wallsBitmaskByteArray = bytearray(wallsBitmaskBytes)
    print("==== wallsBitmaskByteArray hex: 0x" + str(wallsBitmaskByteArray.hex()))
    wallsBitmaskArray = BitArray(hex=wallsBitmaskBytes.hex())
    wallsBitmaskArray.reverse()
    print("==== Cube walls bitmask: " + wallsBitmaskArray.bin)
    for index in list(range(numberOfSidesOnACube)):
        sideHasWall = wallsBitmaskArray[index] == 1
        if(sideHasWall):
            wallIdBytes = data.read(1)
            wallId = int.from_bytes(wallIdBytes, "little")
            wallInfo = WallInfo(wallId, index)
            walls.append(wallInfo)

    # Parse texture info
    cubeTextures = []
    print("######################## Parsing cube textures ########################")
    print("neighbor bitmask: " + cubeNeighborBitmaskArray.bin)
    print("wall bitmask: " + wallsBitmaskArray.bin)
    print("#######################################################################")
    for index in list(range(numberOfSidesOnACube)):
        isDisconnectedSide = cubeNeighborBitmaskArray[index] == 0
        isWallSide = wallsBitmaskArray[index] == 1
        sideHasTexture = isDisconnectedSide or isWallSide
        if(sideHasTexture):
            print("~~~~~~~~~~~ Found textured side: " + str(index) + " ~~~~~~~~~~~~~~`")
            # Get primary texture id
            primaryTextureBytes = data.read(2)
            primaryTextureByteArray = bytearray(primaryTextureBytes)
            primaryTextureByteArray.reverse()
            primaryTextureBits = BitArray(hex=primaryTextureByteArray.hex())
            # print("primaryTextureBits: " + str(primaryTextureBits.bin))
            if(primaryTextureBits[0] == 1):
                secondaryTextureExists = True
            else:
                secondaryTextureExists = False
            primaryTextureBits = primaryTextureBits[1:16]
            primaryTextureId = primaryTextureBits.int
            print("Primary Texture ID: " + str(primaryTextureId))

            # Get secondary texture id            
            secondaryTextureId = None
            if(secondaryTextureExists):
                secondaryTextureBytes = data.read(2)
                secondaryTextureId = int.from_bytes(secondaryTextureBytes, "little")
            print("Secondary Texture ID " + str(secondaryTextureId))

            textureInfo = TextureInfo(primaryTextureId, secondaryTextureId, index)
            cubeTextures.append(textureInfo)

            # TODO: Get UVL value(s)
            # For now, just ignore the values
            numBytesForUVL = 12 * 2
            junk = data.read(numBytesForUVL)
    
    print("\n")

    # Store the cube data
    cubeId = cubeIndex
    cube = Cube(cubeId, neighborCubes, isEnergyCenter, vertexIndices, energyCenterInfo, staticLightFP, walls, cubeTextures)
    cubes.append(cube)


# Print out the cube info
for cube in cubes:
    print("\n")
    print("=========Cube Info=========")
    print("Cube id: " + str(cube.id))
    print("Is Energy Center: " + str(cube.isEnergyCenter))
    print("Neighbors:")
    for neighborCube in cube.neighborCubes:
        print("Id: " + str(neighborCube._attachedCubeId) + ", Side: " + str(CubeSide(neighborCube._cubeSide)))

    print("Vertex Indices:")
    for vertexIndex in cube.vertexIndices:
        print(vertexIndex)

    if(cube.energyCenterInfo is not None):
        print("Energy Center Info:")
        print("Special: " + str(cube.energyCenterInfo.special))
        print("Energy Center Number: " + str(cube.energyCenterInfo.energyCenterNumber))
        print("Value: " + str(cube.energyCenterInfo.value))

    print("Static light value: " + str(float(cube.staticLightFP)))

    print("Walls:")
    for wall in cube.wallInfoList:
        print("Id: " + str(wall.wallId) + ", Side: " + str(CubeSide(wall.cubeSide)))

    print("Textures:")
    for texture in cube.textureInfoList:
        print("=== Textures for side: " + str(texture.cubeSide) + " ===")
        print("Primary Texture: " + str(texture.primaryTextureId))
        print("Secondary Texture: " + str(texture.secondaryTextureId))

# Output obj file
obj = ""
for vertex in vertexCoords:
    obj += "v " + str(float(vertex[0])) + " " + str(float(vertex[1])) + " " + str(float(vertex[2])) + "\n"
for cube in cubes:
    vertexIndices = cube.vertexIndices
    front_1 = [vertexIndices[VertexPosition.LEFT_FRONT_TOP.value]+1, vertexIndices[VertexPosition.LEFT_FRONT_BOTTOM.value]+1, vertexIndices[VertexPosition.RIGHT_FRONT_BOTTOM.value]+1]
    front_2 = [vertexIndices[VertexPosition.RIGHT_FRONT_BOTTOM.value]+1, vertexIndices[VertexPosition.RIGHT_FRONT_TOP.value]+1, vertexIndices[VertexPosition.LEFT_FRONT_TOP.value]+1]
    back_1 = [vertexIndices[VertexPosition.RIGHT_BACK_BOTTOM.value]+1, vertexIndices[VertexPosition.LEFT_BACK_BOTTOM.value]+1, vertexIndices[VertexPosition.LEFT_BACK_TOP.value]+1]
    back_2 = [vertexIndices[VertexPosition.LEFT_BACK_TOP.value]+1, vertexIndices[VertexPosition.RIGHT_BACK_TOP.value]+1, vertexIndices[VertexPosition.RIGHT_BACK_BOTTOM.value]+1]
    top_1 = [vertexIndices[VertexPosition.LEFT_BACK_TOP.value]+1, vertexIndices[VertexPosition.LEFT_FRONT_TOP.value]+1, vertexIndices[VertexPosition.RIGHT_FRONT_TOP.value]+1]
    top_2 = [vertexIndices[VertexPosition.RIGHT_FRONT_TOP.value]+1, vertexIndices[VertexPosition.RIGHT_BACK_TOP.value]+1, vertexIndices[VertexPosition.LEFT_BACK_TOP.value]+1]
    bottom_1 = [vertexIndices[VertexPosition.LEFT_FRONT_BOTTOM.value]+1, vertexIndices[VertexPosition.LEFT_BACK_BOTTOM.value]+1, vertexIndices[VertexPosition.RIGHT_BACK_BOTTOM.value]+1]
    bottom_2 = [vertexIndices[VertexPosition.RIGHT_BACK_BOTTOM.value]+1, vertexIndices[VertexPosition.RIGHT_FRONT_BOTTOM.value]+1, vertexIndices[VertexPosition.LEFT_FRONT_BOTTOM.value]+1]
    right_1 = [vertexIndices[VertexPosition.RIGHT_FRONT_BOTTOM.value]+1, vertexIndices[VertexPosition.RIGHT_BACK_BOTTOM.value]+1, vertexIndices[VertexPosition.RIGHT_BACK_TOP.value]+1]
    right_2 = [vertexIndices[VertexPosition.RIGHT_BACK_TOP.value]+1, vertexIndices[VertexPosition.RIGHT_FRONT_TOP.value]+1, vertexIndices[VertexPosition.RIGHT_FRONT_BOTTOM.value]+1]
    left_1 = [vertexIndices[VertexPosition.LEFT_FRONT_BOTTOM.value]+1, vertexIndices[VertexPosition.LEFT_FRONT_TOP.value]+1, vertexIndices[VertexPosition.LEFT_BACK_TOP.value]+1]
    left_2 = [vertexIndices[VertexPosition.LEFT_BACK_TOP.value]+1, vertexIndices[VertexPosition.LEFT_BACK_BOTTOM.value]+1, vertexIndices[VertexPosition.LEFT_FRONT_BOTTOM.value]+1]
    
    obj += "f " + str(front_1[0]) + " " + str(front_1[1]) + " " + str(front_1[2]) + "\n"
    obj += "f " + str(front_2[0]) + " " + str(front_2[1]) + " " + str(front_2[2]) + "\n"
    obj += "f " + str(back_1[0]) + " " + str(back_1[1]) + " " + str(back_1[2]) + "\n"
    obj += "f " + str(back_2[0]) + " " + str(back_2[1]) + " " + str(back_2[2]) + "\n"
    obj += "f " + str(top_1[0]) + " " + str(top_1[1]) + " " + str(top_1[2]) + "\n"
    obj += "f " + str(top_2[0]) + " " + str(top_2[1]) + " " + str(top_2[2]) + "\n"
    obj += "f " + str(bottom_1[0]) + " " + str(bottom_1[1]) + " " + str(bottom_1[2]) + "\n"
    obj += "f " + str(bottom_2[0]) + " " + str(bottom_2[1]) + " " + str(bottom_2[2]) + "\n"
    obj += "f " + str(right_1[0]) + " " + str(right_1[1]) + " " + str(right_1[2]) + "\n"
    obj += "f " + str(right_2[0]) + " " + str(right_2[1]) + " " + str(right_2[2]) + "\n"
    obj += "f " + str(left_1[0]) + " " + str(left_1[1]) + " " + str(left_1[2]) + "\n"
    obj += "f " + str(left_2[0]) + " " + str(left_2[1]) + " " + str(left_2[2]) + "\n"
    
obj += "\n"

print("OBJ:")
print(obj)

if(outputFileName != None):
    f = open(outputFileName, "w")
    f.write(obj)
    f.close()

# Print file header info again (so that it is at the bottom of output)
print("\n")
print("Level Info (from header):")
print("Signature: " + str(signature, "utf8"))
print("Version: " + str(version))
print("Mine data offset: " + str(mineDataOffset))
print("Objects offset: " + str(objectsOffset))
print("File size: " + str(fileSize))
print("Vertex count: " + str(vertexCount))
print("Cube count: " + str(cubeCount))

print("\n")
print("Level Data (parsed):")
print("Vertices: " + str(len(vertexCoords)))
print("Cubes: " + str(len(cubes)))
