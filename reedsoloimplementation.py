# reedsoloimplementation.py
import reedsolo

def apply_reed_solo(data_codewords):
    rs = reedsolo.RSCodec(7)
    # Convert the list of integers to a bytearray as reedsolo expects bytes-like input
    encoded = rs.encode(bytearray(data_codewords))
    return (list(encoded))