import io

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
