import wave
import os

def hide_data(audio_path, data_bytes):
    audio = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    binary_data = ''.join(format(byte, '08b') for byte in data_bytes)
    binary_data += '1111111111111110'  # Delimiter

    for i in range(len(binary_data)):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(binary_data[i])

    modified_audio = wave.open(os.path.join("output", os.path.basename(audio_path)), 'wb')
    modified_audio.setparams(audio.getparams())
    modified_audio.writeframes(frame_bytes)
    modified_audio.close()
    audio.close()
    return os.path.join("output", os.path.basename(audio_path))

def extract_data(audio_path):
    audio = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    binary_data = ''

    for byte in frame_bytes:
        binary_data += str(byte & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted = bytearray()

    for byte in all_bytes:
        if byte == '11111110':
            break
        extracted.append(int(byte, 2))

    audio.close()
    return bytes(extracted)

