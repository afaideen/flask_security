




# These tables are excatly the same, except the [-2] element. It depends on the
# version of the bootloader library you are using on your PIC MCU.
from binascii import unhexlify

from flaskapp import cache

CRC_TABLE = [
    [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
     0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1c1, 0xf1ef],
    [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
     0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef]]

DEBUG_LEVEL = 0
CRC_INDEX = 1
# Should be equal to Device Erase size
ERASE_SIZE        = 16384



def convertByte2Str(xbyte):
    m = ''
    for x in xbyte:
        m = m + chr(x)
    return m


def convertStr2Byte(d):
    m = bytearray()

    for c in d:
        m.append(ord(c))
    return m

def get_checksum_str(payload):
    o = ''
    for c in payload:
        x = hex(ord(c))
        o = o + "%s" % (x[2:])

    return o

def crc16_len(data, len):
    """Calculate the CRC-16 for a string"""
    i = 0
    crc = 0
    for byte in data:
        if len == 0:
            break

        i = (crc >> 12) ^ (ord(byte) >> 4)
        crc = CRC_TABLE[CRC_INDEX][i & 0x0f] ^ (crc << 4)
        # crc = CRC_TABLE[CRC_INDEX][i & 0x0f] ^ (crc << 4) & 0xffff
        i = (crc >> 12) ^ (ord(byte) >> 0)
        crc = CRC_TABLE[CRC_INDEX][i & 0x0f] ^ (crc << 4)
        # crc = CRC_TABLE[CRC_INDEX][i & 0x0f] ^ (crc << 4) & 0xffff
        len = len - 1
        crc = crc & 0xffff

    return chr(crc & 0xff) + chr((crc >> 8) & 0xff)


def calculate_checksum(data):
    l = ['\xff'] * 4096 * 128

    data_ = data.split('\n')
    data_len = 0
    curr_len = 0
    v_ = ''
    low_addr = ''
    cnt = 0
    i = 0
    j = 0
    g = 0
    for d in data_:
        d = d.strip()
        cnt = cnt + 1
        if len(d) == 0:
            E = 1
            break
        if ':0000' in d:
            E = 1
            continue

        if ':020000' in d:
            E = 1

            q = d[-6:-2]
            if q == '0000':
                low_addr = q
                # g = 1
            else:
                # g = 0
                if low_addr == '':
                    low_addr = '0000'
                hi_addr = q[2:]
                addr = int(hi_addr + low_addr, 16)
                E = 1
            continue

        addr1 = addr + int(d[3:7], 16) - 16
        # addr1 = addr1 - 16
        if addr1 < 0:
            E = 1

        v = unhexlify(d[9:-2])
        v_str = (convertByte2Str(v))

        for k in v_str:
            l[addr1] = k
            addr1 = addr1 + 1

        if addr1 >= curr_len:
            curr_len = addr1
        E = 1

    v_ = ''.join([str(elem) for elem in l])

    data_len = curr_len
    c = crc16_len(v_, data_len)
    x1 = hex(ord(c[0]))
    x2 = hex(ord(c[1]))
    hexcrc = c[0] + c[1]
    p = get_checksum_str(hexcrc).zfill(4)
    E = 1
    print("crc16: OX%s, len: %d" % (p, data_len))
    return p, data_len

def upload_data(ip_address, conn_stream, original_data):
    data_list = original_data.split('\r\n')
    count = 0
    data_size = 0
    data = bytearray()
    txcount, rxcount, txsize, rxsize = 0, 0, 0, 0
    crc = 0
    for d in data_list:
        d = d.strip()
        v = unhexlify(d[1:])
        data.extend(v)
        data_size = data_size + len(v)
        data_str = convertByte2Str(data)
        if count > 0 and \
                (
                        count % 20 == 0 \
                        or ":0000" in d
                ):
            print("sending data..%d\r\n" % (txcount))
            txsize += conn_stream.send_request('\x03' + data_str, txcount)
            response = conn_stream.read_response('\x03')
            rxsize += len(response) + 4
            txcount += 1
            rxcount += 1

            v = count / len(data_list) * 100
            progress_bar_value = str(round(v))
            cache.set('progress_bar_value_' + ip_address, progress_bar_value)
            print("Progress value: %s%%" % (progress_bar_value))
            data = bytearray()
        count += 1
        print('*')

    return (txcount, txsize, rxcount, rxsize, data_size)
