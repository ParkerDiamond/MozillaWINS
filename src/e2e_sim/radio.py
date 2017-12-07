import zlib
import random

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

    # TODO turbo encode txdata

    rxdata = corrupt(txdata, error)

    # TODO turbo decode rxdata

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

