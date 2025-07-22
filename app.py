from flask import Flask, render_template, request, send_file
import io
import os
import encoder
import reedsoloimplementation
import matrixbuilder
import MatrixToImage

app = Flask(__name__)
qr_image_global = None  # to store the qr image

@app.route('/', methods=['GET', 'POST'])
def index():
    global qr_image_global
    encoded_output = None
    bit_length = 0

    if request.method == 'POST':
        user_text = request.form['qr_text']
        show_steps = 'show_steps' in request.form
        print(f"user_text: {user_text}")
        print("Show steps:", show_steps)

        # 🎨 Get colour and size selections
        fg_color = request.form.get('fg_color', '#000000')
        bg_color = request.form.get('bg_color', '#ffffff')
        module_size = int(request.form.get('module_size', '10'))

        # Version selection
        if len(user_text.encode('utf-8')) > 17:
            version_bits = 304
            print("Using Version 2")
        else:
            version_bits = encoder.VERSION_1_LEVEL_L_CAPACITY_BITS
            print("Using Version 1")

        data_codewords, padded_bit_string = encoder.prepare_qr_data_stream(
            user_text, version_bits
        )
        reed_check = reedsoloimplementation.apply_reed_solo(data_codewords)
        print(f"Reed-Solomon encoded codewords: {reed_check}")
        encoded_output = reed_check

        matrix = matrixbuilder.build_matrix(reed_check, user_text, show_steps)

        for row in matrix:
            print(''.join(['#' if cell == 1 else ' ' if cell == 0 else '.' for cell in row]))

        bit_length = len(padded_bit_string)

        # 🖼️ Generate image with custom colours and scale
        qr_image = MatrixToImage.matrix_to_image(matrix, fg=fg_color, bg=bg_color, scale=module_size)
        qr_image_global = io.BytesIO()
        qr_image.save(qr_image_global, format='PNG')
        qr_image_global.seek(0)

    return render_template('index.html', encoded_output=encoded_output, bit_length=bit_length, qr_code_image=True)

@app.route('/qr_image')
def qr_image():
    if qr_image_global:
        qr_image_global.seek(0)
        return send_file(qr_image_global, mimetype='image/png')
    else:
        return "No QR code found", 404

@app.route('/qr_steps')
def qr_steps():
    steps_dir = os.path.join(app.static_folder, 'steps')
    if not os.path.exists(steps_dir):
        step_files = []
    else:
        step_files = sorted(f for f in os.listdir(steps_dir) if f.endswith('.png'))
    return render_template('qr_steps.html', step_files=step_files)

if __name__ == '__main__':
    app.run(debug=True)
