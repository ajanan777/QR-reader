from enhancements import enhance_qr

def create_empty_matrix(size=21):
    return [[None for _ in range(size)] for _ in range(size)]

def add_finder_pattern(matrix, top, left):
    pattern = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
    for r in range(7):
        for c in range(7):
            matrix[top + r][left + c] = pattern[r][c]

def add_separators(matrix):
    positions = [(0, 0), (0, 14), (14, 0)]
    for top, left in positions:
        for i in range(-1, 8):
            if 0 <= left + i < 21:
                if top - 1 >= 0:
                    matrix[top - 1][left + i] = 0
                if top + 7 < 21:
                    matrix[top + 7][left + i] = 0
        for j in range(-1, 8):
            if 0 <= top + j < 21:
                if left - 1 >= 0:
                    matrix[top + j][left - 1] = 0
                if left + 7 < 21:
                    matrix[top + j][left + 7] = 0

def add_all_finder_patterns(matrix):
    add_finder_pattern(matrix, 0, 0)
    add_finder_pattern(matrix, 0, 14)
    add_finder_pattern(matrix, 14, 0)
    add_separators(matrix)

def add_timing_patterns(matrix):
    val = 1
    for i in range(8, 13):
        matrix[6][i] = val
        val = 1 - val
    val = 1
    for j in range(8, 13):
        matrix[j][6] = val
        val = 1 - val

def add_dark_module(matrix):
    matrix[13][8] = 1

def add_format_information(matrix):
    format_bits = "111011111000100"
    for i in range(0, 7):
        matrix[20 - i][8] = int(format_bits[i])
    for i in range(7, 15):
        matrix[8][13 - 7 + i] = int(format_bits[i])
    matrix[8][8] = int(format_bits[7])
    matrix[7][8] = int(format_bits[8])
    for i in range(9, 15):
        matrix[9 + 5 - i][8] = int(format_bits[i])
    for i in range(0, 6):
        matrix[8][0 + i] = int(format_bits[i])
    matrix[8][7] = int(format_bits[6])

def add_data_bits(matrix, codewords):
    size = len(matrix)
    bit_string = ''.join(f"{cw:08b}" for cw in codewords)
    bit_idx = 0
    total_bits = len(bit_string)

    col = size - 1
    while col > 0 and bit_idx < total_bits:
        if col == 6:
            col -= 1

        cols = [col, col - 1]
        pair_index = (size - 1 - col) // 2
        upward = (pair_index % 2 == 0)
        rows = range(size - 1, -1, -1) if upward else range(size)

        for r in rows:
            for c in cols:
                if matrix[r][c] is None and bit_idx < total_bits:
                    matrix[r][c] = int(bit_string[bit_idx])
                    bit_idx += 1
        col -= 2
    return matrix

def apply_mask_pattern_0(matrix):
    size = len(matrix)
    for r in range(size):
        for c in range(size):
            if r == 6 or c == 6:
                continue
            if r < 9 and c < 9:
                continue
            if r < 9 and c >= size - 8:
                continue
            if r >= size - 8 and c < 9:
                continue
            if r == 13 and c == 8:
                continue
            if matrix[r][c] is not None:
                if (r + c) % 2 == 0:
                    matrix[r][c] = 1 - matrix[r][c]

# ✅ Updated to accept third argument
def build_matrix(all_codewords, input_text, show_steps=False):
    version1_matrix = create_empty_matrix()
    add_all_finder_patterns(version1_matrix)
    add_timing_patterns(version1_matrix)
    add_dark_module(version1_matrix)
    add_format_information(version1_matrix)
    add_data_bits(version1_matrix, all_codewords)
    final_matrix = enhance_qr(input_text, version1_matrix, show_steps=show_steps)
    return final_matrix
