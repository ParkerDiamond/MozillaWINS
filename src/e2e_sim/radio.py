import ctypes
import zlib
import random

turbolib = ctypes.cdll.LoadLibrary('../simulation/libsimpleturbo.so')

def corrupt(data, error):
    # Check each bit for random error
    data = bytearray(data)
    for byte in range(len(data)):
        for bit in range(8):
            if random.random() < error:
                data[byte] ^= 0x1 << bit
    return bytes(data)

def attempt_transmission(data, error):
    if type(data) != bytes:
        data = data.encode('utf-8')

    tcdata = zlib.compress(data, 9)
    tcsum = zlib.crc32(data)

    txdata = tcdata + tcsum.to_bytes(4, byteorder='big')

    rxdata = turbo_transmit(txdata, error)

    rcdata, rcsum = rxdata[:-4], int.from_bytes(rxdata[-4:], 'big')

    try:
        rdata = zlib.decompress(rcdata)
    except zlib.error:
        print('failed decompression')
        return False, 0

    if zlib.crc32(rdata) != rcsum:
        print('bad checksum')
        return False, 0

    return True, len(txdata)


def turbo_transmit(data, error):
    return data
    if type(data) == str:
        data = data.encode('utf-8')
    c_data = ctypes.c_char_p(data)
    c_error = ctypes.c_double(error)

    turbolib.transmit(c_data, len(data), c_error)

    return data



