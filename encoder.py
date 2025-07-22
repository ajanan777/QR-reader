def encode_text(text):
    byte_data = text.encode('utf-8')
    binary_string = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_string, len(byte_data) * 8

def len_encoder_text(text):
    return len(text.encode('utf-8')) * 8

# Version 1, Error Correction Level L Information:
VERSION_1_LEVEL_L_CAPACITY_BITS = 152

def pad_data(bit_string, capacity_bits):
    padded_bits = bit_string + '0000'  # Add terminator (up to 4 '0's)

    remainder = len(padded_bits) % 8
    if remainder != 0:
        padded_bits += '0' * (8 - remainder)

    # Add pad bytes until capacity is reached (using decimal values 236 and 17)
    while len(padded_bits) < capacity_bits:
        padded_bits += format(236, '08b')  # Pad byte 1 (11101100)
        if len(padded_bits) < capacity_bits:
            padded_bits += format(17, '08b')   # Pad byte 2 (00010001)

    return padded_bits[:capacity_bits] # Truncate if over capacity

def bits_to_codewords(padded_bits):
    codewords = [int(padded_bits[i:i+8], 2) for i in range(0, len(padded_bits), 8)]
    return codewords

# --- NEW FUNCTION TO ORCHESTRATE DATA PREPARATION ---
def prepare_qr_data_stream(text, version_capacity_bits):
    # 1. Encode the original text into a binary string
    encoded_data_bits, total_data_bits_length = encode_text(text)

    # 2. Determine Character Count
    # For Byte mode (UTF-8), the character count is simply the number of bytes.
    # len(text.encode('utf-8')) gives the number of bytes.
    character_count = len(text.encode('utf-8'))

    # 3. Add Mode Indicator (4 bits)
    # For 'Byte' mode (which UTF-8 falls under), the mode indicator is '0100'.
    mode_indicator = '0100'

    # 4. Add Character Count Indicator
    # For QR Code Version 1 in Byte mode, the character count field is 8 bits long.
    # You'll need to check the QR code specification for other versions and modes.
    # Format the character count as an 8-bit binary string, left-padded with zeros.
    character_count_indicator = format(character_count, '08b')

    # 5. Combine the header (mode + count) with the actual encoded data
    data_with_header = mode_indicator + character_count_indicator + encoded_data_bits

    # 6. Pad the combined data stream to the required capacity for the QR version/level
    final_padded_bits = pad_data(data_with_header, version_capacity_bits)

    # 7. Convert the final padded bit stream into 8-bit codewords
    qr_codewords = bits_to_codewords(final_padded_bits)

    return qr_codewords, final_padded_bits