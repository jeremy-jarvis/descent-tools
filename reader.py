import io
from decimal import *
import binascii
from bitstring import BitArray
from fixedpoint import FixedPoint

def convert_coord_bytes_to_decimal(coordBytes):
    # print("coordBytes: " + str(binascii.hexlify(coordBytes)))
    print("coordBytes: " + str(coordBytes))
    bits = BitArray(hex=coordBytes.hex())
    print("The Bits: " + bits.bin)
    print(len(bits.bin))
    # coordBytesBinary = bin(coordBytes)
    # print("coordBytes binary: " + coordBytesBinary)
    # bytesString = "0b" + coordBytes.hex()
    hexString = "0x" + coordBytes.hex()
    print("hexString: " + hexString)
    bitString = "0b" + bits.bin
    print("bitString: " + bitString)
    coordFP = FixedPoint(bitString, signed=1, m=16, n=16, str_base=2)
    a = coordFP
    print(f"{a:#0{a.m+2}bm}.{a:0{a.n}bn}")
    print("coordFP Fixed Point: " + str(float(coordFP)))
    print(coordFP.qformat)
    print(str(coordFP))
    # print("coordBytes array length: " + str(len(coordBytes)))
    # print("First two bytes: " + str(coordBytes[2:4]))
    # print("Second two bytes: " + str(coordBytes[0:2]))
    # intPortion = int.from_bytes(coordBytes[2:4], "big", signed=True)
    # print("int Portion: " + str(intPortion))
    # # fractionPortion = int.from_bytes(coordBytes[0:2], "big")
    # # print("fraction Portion: " + str(fractionPortion))
    # coordinate = intPortion # + fractionPortion
    # return coordinate
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

vertexCountBytes = data.read(2)
vertexCount = int.from_bytes(vertexCountBytes, "big")
print("Vertex count: " + str(vertexCount))

cubeCountBytes = data.read(2)
cubeCount = int.from_bytes(cubeCountBytes, "big")
print("Cube count: " + str(cubeCount))

verticesBytes = data.read(vertexCount * 12) # 12 byes per vertex
print("verticesBytes: " + str(verticesBytes))
# print("=================" + bin(int.from_bytes(verticesBytes, "big")))
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

    xBytes = vertex[2:4] + vertex[0:2]
    yBytes = vertex[6:8] + vertex[4:6]
    zBytes = vertex[10:12] + vertex[8:10]

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


# print("xBytes: " + str(xBytes))
# print("xBytes array length: " + str(len(xBytes)))
# print("First two bytes: " + str(xBytes[0:2]))
# intPortion = int.from_bytes(xBytes[2:4], "big")
# print("int Portion: " + str(intPortion))
# fractionPortion = int.from_bytes(xBytes[0:2], "big")
# print("fraction Portion: " + str(fractionPortion))
# xPos = intPortion + fractionPortion
    
# x = int.from_bytes(xBytes, "big")
# y = int.from_bytes(yBytes, "big")
# z = int.from_bytes(zBytes, "big")
# print("x: " + str(x) + '\n')
# print("y: " + str(y) + '\n')
# print("z: " + str(z) + '\n')
