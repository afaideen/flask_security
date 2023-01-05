




# These tables are excatly the same, except the [-2] element. It depends on the
# version of the bootloader library you are using on your PIC MCU.
from binascii import unhexlify

from flaskapp import cache
from abc import ABCMeta, abstractmethod
import socket

CRC_TABLE = [
    [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
     0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1c1, 0xf1ef],
    [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
     0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef]]

DEBUG_LEVEL = 0
CRC_INDEX = 1
# Should be equal to Device Erase size
ERASE_SIZE        = 16384


class DataStream:
    """Abstract class for interfaces to the chip"""
    __metaclass__ = ABCMeta

    global DEBUG_LEVEL # pylint: disable=global-statement

    def __init__(self):
        pass

    def read_response(self, command):
        """Retrieve response from the chip"""
        response = self.sub_read_response()

        if DEBUG_LEVEL >= 2:
            print('<', hexlify(response))

        if response[0] != ord('\x01') or response[-1] != ord('\x04'):
            raise IOError('Invalid response from bootloader')

        # response1 = unescape(response[1:-1])
        response1 = unescape(response[1:-3])

        # Verify SOH, EOT and command fields
        if response1[0] != ord(command):
            raise IOError('Unexpected response type from bootloader')
        # x = response1.decode()
        x = convertByte2Str(response1)
        y = crc16(x)
        crc_calculated = chr(ord(y[0])) + chr(ord(y[1]))
        crc_original = chr(response[-3:-1][0]) + chr(response[-3:-1][1])
        # if crc16(response1[:-2]) != response1[-2:]:
        if crc_calculated != crc_original:
            raise IOError('Invalid CRC from bootloader')

        # return response1[1:-2]
        if len(response1) == 1:
            return response1
        return response1[1:]


    def send_request(self, command, txcount = None):
        """Build and send request"""
        command1 = escape(command)
        # printX(command1)
        # if '\x03' in command[2:] and ord(command[0]) == 3 and txcount >= 1:
        if '\x03' in command[2:] and ord(command[0]) == 3:
            #if upload only
            command1 = command1[0:2] + command1[2:].replace('\x03', '\x10\x03')
            # printX(command1)
        # if ord(command[0]) == 4:
        #     print(convert(command1))
        #     crc_cmd1 = escape(crc16(command1))
        #     print(convert(crc_cmd1))
        crc = crc16(command)
        request = '\x01' + command1 + escape(crc) + '\x04'
        result = convert(request)
        # printX(request)
        self.sub_send_request(request)

        if DEBUG_LEVEL >= 2:
            print('>', hexlify(request))

        return len(request)

    @abstractmethod
    def sub_read_response(self):
        """Implementation-specific method to retrieve data from the chip"""
        pass

    @abstractmethod
    def sub_send_request(self, request):
        """Implementation-specific method to send data to the chip"""
        pass
class UDPStream(DataStream):
    """UDP interface"""

    def __init__(self, udp_addr, udp_port, timeout):
        self.udp_addr = udp_addr
        self.udp_port = udp_port
        self.timeout = timeout
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soc.settimeout(self.timeout)

        super(UDPStream, self).__init__()

    def sub_read_response(self):
        try:
            response, _ = self.soc.recvfrom(1024)
            return response
        except Exception:
            raise IOError('Bootloader response timed out')

    def sub_send_request(self, request):
        # request = str.encode(request)
        data = convertStr2Byte(request)

        self.soc.sendto(data, (self.udp_addr, self.udp_port))



def crc16(data):
    """Calculate the CRC-16 for a string"""
    i = 0
    crc = 0
    for byte in data:
        i = (crc >> 12) ^ (ord(byte) >> 4)
        # crc = CRC_TABLE[CRC_INDEX][i & 0x0f] ^ (crc << 4)
        crc = CRC_TABLE[CRC_INDEX][i & 0x0f] ^ (crc << 4) & 0xffff
        i = (crc >> 12) ^ (ord(byte) >> 0)
        # crc = CRC_TABLE[CRC_INDEX][i & 0x0f] ^ (crc << 4)
        crc = CRC_TABLE[CRC_INDEX][i & 0x0f] ^ (crc << 4) & 0xffff

    return chr(crc & 0xff) + chr((crc >> 8) & 0xff)

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

def parse_args():
    """Parse command line arguments"""
    pars = ArgumentParser(formatter_class=RawTextHelpFormatter)

    pars.add_argument(
        '-i', '--interface',
        help='Choose bootloader communication interface',
        choices=['uart', 'udp'],
        required=True)

    pars.add_argument(
        '-a', '--udp-addr',
        help='IP Address for UDP')
    pars.add_argument(
        '-n', '--udp-port',
        help='UDP port number',
        type=int, default=6234)

    pars.add_argument(
        '-p', '--port',
        help='Serial port to use')
    pars.add_argument(
        '-b', '--baud',
        help='Baudrate to the bootloader',
        type=int, default=115200)

    pars.add_argument(
        '-u', '--upload',
        help='Upload file to chip',
        metavar='firmware.hex')
    pars.add_argument(
        '-c', '--check',
        help='Check CRC of a memory block ADDR:SIZE\n'\
             '  ADDR - 32 bit start address (hex)\n'\
             '  SIZE - 32 bit block length in bytes',
        type=str, default='9d000000:000000ff',
        nargs='?')
    pars.add_argument(
        '-e', '--erase',
        help='Erase before upload',
        action='store_true')
    pars.add_argument(
        '-r', '--run',
        help='Run after upload',
        action='store_true')
    pars.add_argument(
        '-v', '--version',
        help='Read bootloader version',
        action='store_true')

    pars.add_argument(
        '-t', '--timeout',
        help='Timeout in seconds',
        type=float, default=1.0)
    pars.add_argument(
        '-D', '--debug',
        help='Debug level',
        type=int, default=0)

    pars.add_argument(
        '--my-version',
        action='version',
        version='%(prog)s ' + __version__)

    pars.add_argument(
        '--crc',
        help='CRC table',
        choices=['0', '1'],
        default=1)

    return pars.parse_args()



def escape(data):
    """Escape control characters"""
    data = data.replace('\x10', '\x10\x10')
    data = data.replace('\x01', '\x10\x01')
    # data = data.replace('\x03', '\x10\x03')
    data = data.replace('\x04', '\x10\x04')
    return data

def unescape(data):
    """Inverse of escape"""
    escaping = False
    record = ''
    for byte in list(data):
        if escaping:
            record += chr(byte)
            escaping = False
        elif chr(byte) == '\x10' or chr(byte) == '\x01' or chr(byte) == '\x04':
            escaping = True
        else:
            record += chr(byte)
    # record2 = str.encode(record)
    record2 = convertStr2Byte(record)
    return record2

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

def convert(payload):
    r = ''
    for c in payload:
        x = hex(ord(c))
        r = r + "\\" + x
    return r

def get_checksum_str(payload):
    o = ''
    for c in payload:
        x = hex(ord(c))
        o = o + "%s" % (x[2:])

    return o


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
                        count % 20 == 0
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

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

