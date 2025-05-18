from PIL import Image
import os
import struct  # for packing/unpacking length prefix

def calculate_capacity(image_path):
    img = Image.open(image_path)
    pixels = img.size[0] * img.size[1]
    capacity_bits = pixels * 3  # 3 bits per pixel (R,G,B)
    capacity_bytes = capacity_bits // 8  # bits to bytes
    return capacity_bytes

def hide_data(image_path, data_bytes):
    img = Image.open(image_path)
    encoded = img.copy()

    # Prepend 4-byte length header to data_bytes
    length_prefix = struct.pack('>I', len(data_bytes))  # big-endian unsigned int
    data_with_len = length_prefix + data_bytes

    binary_data = ''.join(format(byte, '08b') for byte in data_with_len)

    capacity = calculate_capacity(image_path)
    if len(data_with_len) > capacity:
        raise ValueError(f"Data too large to hide! Capacity: {capacity} bytes, Data size: {len(data_with_len)} bytes")

    data_index = 0
    pixels = encoded.getdata()
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel[:3]
        if data_index < len(binary_data):
            r = (r & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            g = (g & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            b = (b & ~1) | int(binary_data[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    encoded.putdata(new_pixels)
    out_path = os.path.join("output", os.path.basename(image_path))
    encoded.save(out_path)
    return out_path

def extract_data(image_path):
    img = Image.open(image_path)
    binary_data = ''
    for pixel in img.getdata():
        r, g, b = pixel[:3]
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)

    # Extract length prefix first 4 bytes = 32 bits
    length_bits = binary_data[:32]
    data_length = int(length_bits, 2)

    # Now extract exactly data_length bytes * 8 bits after the prefix
    total_data_bits = 32 + data_length * 8
    data_bits = binary_data[32:total_data_bits]

    all_bytes = [data_bits[i:i+8] for i in range(0, len(data_bits), 8)]
    extracted = bytearray()

    for byte in all_bytes:
        extracted.append(int(byte, 2))

    return bytes(extracted)
