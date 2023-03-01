import json
import sys, getopt, os
import struct
import subprocess

f = open(sys.argv[1])
f2 = open(sys.argv[2], 'rb')

data = json.load(f)

shaders = data['SerializedShaders']
hashes = shaders['ShaderMapHashes']
index = hashes.index(sys.argv[3])

map_entry = shaders['ShaderMapEntries'][index]
offset = map_entry['ShaderIndicesOffset']
num = map_entry['NumShaders']

shader_index = 0

for n in range(offset, offset + num):
    shader_entry = shaders['ShaderEntries'][n]
    offset = shader_entry['Offset']
    size = shader_entry['Size']
    uncompressed_size = shader_entry['UncompressedSize']
    f2.seek(4, 0)
    map_array_size = struct.unpack('i', f2.read(4))[0]
    f2.seek(20 * map_array_size, 1)
    shader_array_size = struct.unpack('i', f2.read(4))[0]
    f2.seek(20 * shader_array_size, 1)
    f2.seek(16 * map_array_size + 4, 1)
    f2.seek(17 * shader_array_size + 4, 1)
    preload_array_size = struct.unpack('i', f2.read(4))[0]
    f2.seek(16 * preload_array_size, 1)
    shader_indices_size = struct.unpack('i', f2.read(4))[0]
    f2.seek(4 * shader_indices_size, 1)
    f2.seek(offset, 1)
    data = bytearray()
    data += f2.read(size)
    o = open(sys.argv[4] + str(shader_index), "wb")
    o.write(data)
    o.close()
    subprocess.call(['decompress_shader.exe', sys.argv[4] + str(shader_index), str(uncompressed_size)])
    os.remove(sys.argv[4] + str(shader_index))
    shader_index += 1

f.close()
