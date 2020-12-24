import io

empty_bytes = bytes(4)
print(type(empty_bytes))
print(empty_bytes)

mutable_bytes = bytearray(b'\x00\x0f')
print(mutable_bytes)
mutable_bytes[0] = 255
mutable_bytes.append(255)
print(mutable_bytes)

immutable_bytes = bytes(mutable_bytes)
print(immutable_bytes)

binary_stream = io.BytesIO()
binary_stream.write("Hello, world!\n".encode('ascii'))
binary_stream.write("Hello, world!\n".encode('utf-8'))
binary_stream.seek(0)
stream_data = binary_stream.read()
print(type(stream_data))
print(stream_data)

mutable_buffer = binary_stream.getbuffer()
print(type(mutable_buffer))
mutable_buffer[0] = 0xFF

binary_stream.seek(0)
print(binary_stream.read())