import os
from encoder import prepare_qr_data_stream
from reedsoloimplementation import apply_reed_solo
from MatrixToImage import matrix_to_image

def save_step(matrix, name):
    steps_path = os.path.join("static", "steps")
    os.makedirs(steps_path, exist_ok=True)
    img = matrix_to_image(matrix)
    img.save(os.path.join(steps_path, f"{name}.png"))

def should_use_version_2(input_text):
    return len(input_text.encode('utf-8')) > 17

def add_alignment_pattern(matrix):
    alignment = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    start = len(matrix) - 9
    for r in range(5):
        for c in range(5):
            matrix[start + r][start + c] = alignment[r][c]
    return matrix

def add_finder_pattern(matrix, top, left):
    pattern = [
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1],
    ]
    for r in range(7):
        for c in range(7):
            matrix[top + r][left + c] = pattern[r][c]

def add_separators(matrix):
    size = len(matrix)
    positions = [(0,0), (0, size - 7), (size - 7, 0)]
    for top, left in positions:
        for i in range(-1, 8):
            if 0 <= left + i < size:
                if top - 1 >= 0:
                    matrix[top - 1][left + i] = 0
                if top + 7 < size:
                    matrix[top + 7][left + i] = 0
        for j in range(-1, 8):
            if 0 <= top + j < size:
                if left - 1 >= 0:
                    matrix[top + j][left - 1] = 0
                if left + 7 < size:
                    matrix[top + j][left + 7] = 0

def add_timing_patterns(matrix):
    size = len(matrix)
    val = 1
    for i in range(8, size - 8):
        matrix[6][i] = val
        matrix[i][6] = val
        val = 1 - val

def add_dark_module(matrix):
    matrix[13][8] = 1

def add_format_information(matrix, version=2):
    format_bits = "111011111000100"
    size = len(matrix)
    for i in range(0, 6):
        matrix[8][i] = int(format_bits[i])
        matrix[i][8] = int(format_bits[i])
    matrix[8][7] = int(format_bits[6])
    matrix[8][8] = int(format_bits[7])
    matrix[7][8] = int(format_bits[8])
    for i in range(9, 15):
        matrix[14 - i][8] = int(format_bits[i])
        matrix[8][size - 15 + i] = int(format_bits[i])

def add_data_bits(matrix, codewords):
    bit_string = ''.join(f"{cw:08b}" for cw in codewords)
    bit_idx = 0
    size = len(matrix)
    col = size - 1
    while col > 0 and bit_idx < len(bit_string):
        if col == 6:
            col -= 1
        for row in range(size - 1, -1, -1):
            for c in [col, col - 1]:
                if matrix[row][c] is None and bit_idx < len(bit_string):
                    matrix[row][c] = int(bit_string[bit_idx])
                    bit_idx += 1
        col -= 2

def build_version2_matrix(input_text, save_steps=False):
    size = 25
    matrix = [[None for _ in range(size)] for _ in range(size)]

    add_finder_pattern(matrix, 0, 0)
    add_finder_pattern(matrix, 0, size - 7)
    add_finder_pattern(matrix, size - 7, 0)
    add_separators(matrix)
    if save_steps: save_step(matrix, "1_finder_separators")

    matrix = add_alignment_pattern(matrix)
    if save_steps: save_step(matrix, "2_alignment_pattern")

    add_timing_patterns(matrix)
    if save_steps: save_step(matrix, "3_timing_patterns")

    add_dark_module(matrix)
    if save_steps: save_step(matrix, "4_dark_module")

    data_codewords, _ = prepare_qr_data_stream(input_text, 304)
    codewords_with_ecc = apply_reed_solo(data_codewords)

    add_format_information(matrix)
    if save_steps: save_step(matrix, "5_format_info")

    add_data_bits(matrix, codewords_with_ecc)
    if save_steps: save_step(matrix, "6_data_bits")

    return matrix

# === TEMPORARY DUMMY FINALIZER ===

def enhance_qr(input_text, version1_matrix, show_steps=False):
    """
    TEMPORARY version for Will's commit only.
    Kamal will later add masking and replace this.
    """
    if should_use_version_2(input_text):
        return build_version2_matrix(input_text, save_steps=show_steps)
    return version1_matrix

