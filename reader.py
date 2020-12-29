import io
from decimal import *
import binascii
from bitstring import BitArray
from fixedpoint import FixedPoint

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


with open("cube.rdl", "rb") as level_file:
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

vertexCountBytes = data.read(2)
# print("Vertex count bytes: " + str(vertexCountBytes.hex()))
vertexCount = int.from_bytes(vertexCountBytes, "little")
print("Vertex count: " + str(vertexCount))

cubeCountBytes = data.read(2)
# print("Cube count bytes: " + str(cubeCountBytes.hex()))
cubeCount = int.from_bytes(cubeCountBytes, "little")
print("Cube count: " + str(cubeCount))

verticesBytes = data.read(vertexCount * 12) # 12 byes per vertex
vertices = io.BytesIO(verticesBytes)

for index in list(range(vertexCount)):
    print("=========== VERTEX =============")
    vertexBytes = vertices.read(12)
    vertex = bytearray(vertexBytes)
    print("Length of vertex bytearray: " + str(len(vertex)))
    vertexBits = BitArray(hex=vertex.hex())
    print("vertexBits: " + vertexBits.bin)

    xBytesOriginal = vertex[0:4]
    xBits = BitArray(hex=xBytesOriginal.hex())
    print("Original X Bits: " + xBits.bin)
    print("Original X Bits in Byte form: " + str(xBits.bytes))
    yBytesOriginal = vertex[4:8]
    yBits = BitArray(hex=yBytesOriginal.hex())
    print("Original Y Bits: " + yBits.bin)
    print("Original Y Bits in Byte form: " + str(yBits.bytes))
    zBytesOriginal = vertex[8:12]
    zBits = BitArray(hex=zBytesOriginal.hex())
    print("Original Z Bits: " + zBits.bin)
    print("Original Z Bits in Byte form: " + str(zBits.bytes))

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
