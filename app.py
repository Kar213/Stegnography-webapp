from flask import Flask, render_template, request, send_file
import os
import struct
import uuid
from zipfile import ZipFile
from steg_utils import image_stego, audio_stego, video_stego, crypto_utils

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def handle_form():
    mode = request.form.get('mode')
    encryption_method = request.form.get('encryption')
    data_type = request.form.get('data_type')
    carrier_file = request.files.get('carrier')

    if not carrier_file or carrier_file.filename == "":
        return "No carrier file uploaded!", 400

    password = request.form.get('password') or request.form.get('decryption_key')

    carrier_filename = str(uuid.uuid4()) + "_" + carrier_file.filename
    carrier_path = os.path.join(app.config['UPLOAD_FOLDER'], carrier_filename)
    carrier_file.save(carrier_path)

    file_ext = carrier_file.filename.rsplit('.', 1)[-1].lower()
    if file_ext in ['png', 'jpg', 'jpeg']:
        module = image_stego
    elif file_ext in ['wav', 'mp3']:
        module = audio_stego
    elif file_ext in ['mp4', 'avi']:
        module = video_stego
    else:
        return "Unsupported carrier file type", 400

    if mode == 'encrypt':
        if data_type == 'text':
            text_payload = request.form.get('text_payload')
            if not text_payload:
                return "No text payload provided!", 400
            payload = text_payload.encode()
            original_filename = "hidden_text.txt"
        elif data_type == 'file':
            file_payload = request.files.get('file_payload')
            if not file_payload or file_payload.filename == "":
                return "No file payload provided!", 400
            payload = file_payload.read()
            original_filename = file_payload.filename
        else:
            return "Invalid payload type", 400

        filename_bytes = original_filename.encode()
        filename_len = len(filename_bytes)
        payload_with_name = struct.pack('>I', filename_len) + filename_bytes + payload

        capacity = module.calculate_capacity(carrier_path)

        if encryption_method == 'password':
            if not password:
                return "Password required for password encryption!", 400
            encrypted_data = crypto_utils.encrypt_with_password(payload_with_name, password)
        else:
            # ✅ Now this will work
            encrypted_data, rand_key = crypto_utils.encrypt_with_random_key(payload_with_name)

        if len(encrypted_data) + 4 > capacity:
            return f"Carrier file too small! Capacity: {capacity} bytes, encrypted data size: {len(encrypted_data)+4} bytes", 400

        output_file = module.hide_data(carrier_path, encrypted_data)

        if encryption_method == 'password':
            return send_file(output_file, as_attachment=True, download_name='steg_encoded.' + file_ext)
        else:
            key_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'encryption_key.txt')
            with open(key_file_path, 'w') as f:
                f.write(rand_key)

            zip_path = os.path.join(app.config['OUTPUT_FOLDER'], 'steg_package.zip')
            with ZipFile(zip_path, 'w') as zipf:
                zipf.write(output_file, arcname='steg_encoded.' + file_ext)
                zipf.write(key_file_path, arcname='encryption_key.txt')

            return send_file(zip_path, as_attachment=True, download_name="steg_package.zip")

    elif mode == 'decrypt':
        if not password:
            return "Password or key is required for decryption!", 400

        extracted_data = module.extract_data(carrier_path)
        if not extracted_data:
            return "No hidden data found in the carrier file!", 400

        try:
            if encryption_method == 'password':
                decrypted = crypto_utils.decrypt_with_password(extracted_data, password)
            else:
                decrypted = crypto_utils.decrypt_with_key(extracted_data, password)
        except ValueError as e:
            return str(e), 400

        if len(decrypted) < 4:
            return "Decrypted data corrupted or incomplete", 400

        filename_len = struct.unpack('>I', decrypted[:4])[0]
        if len(decrypted) < 4 + filename_len:
            return "Decrypted data corrupted or incomplete", 400

        original_filename = decrypted[4:4+filename_len].decode()
        actual_payload = decrypted[4+filename_len:]

        output_file = os.path.join(app.config['OUTPUT_FOLDER'], original_filename)
        with open(output_file, 'wb') as f:
            f.write(actual_payload)

        return send_file(output_file, as_attachment=True, download_name=original_filename)

    else:
        return "Invalid mode", 400

if __name__ == '__main__':
    app.run(debug=True)
