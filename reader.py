import io

with open("cube.rdl", "rb") as level_file:
    dataBytes = level_file.read()
    
# data = bytearray(dataBytes)
# print(type(data))
# print(data)

data = io.BytesIO(dataBytes)

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
