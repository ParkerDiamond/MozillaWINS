import zlib

def attempt_transmission(data, error):
    # TODO: apply compression, encode, and error. Then decode and check if correct
    # for now just pretend we transmit data as-is w/ 100% success

    if type(data) != bytes:
        data = data.encode('utf-8')

    cdata = zlib.compress(data, 9)
    return True, len(cdata)
    
