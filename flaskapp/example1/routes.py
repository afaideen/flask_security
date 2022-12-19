import secrets
import time
from binascii import hexlify, unhexlify

from flask_login import current_user, login_required
from flask import render_template, Blueprint, redirect, url_for, session, jsonify, request
from flaskapp.example1.form import UpdateFileForm
from flaskapp import cache
from flaskapp.example1.utils import convertByte2Str, calculate_checksum, upload_data, UDPStream


example1 = Blueprint('example1', __name__)

CMD_READ_VERSION            = "\x01"
CMD_ERASE                   = "\x02"
CMD_FLASH_DATA              = "\x03"
CMD_VERIFY_CS               = "\x04"
CMD_JUMP_APP                = "\x05"
CONFIG_TIME_SIM_SPEED       = 0.5

@example1.route("/run_app/<string:ip_board>", methods=['GET'])
@login_required
def run_app(ip_board):
    try:
        conn_stream = UDPStream(ip_board, 6234, 15)  # 15s timeout
        conn_stream.send_request(CMD_JUMP_APP)
        # r = conn_stream.read_response('\x05')
        print('Device bootloaded successful..')
        status = 'success'
    except Exception as err:
        status = 'fail'
        print('Oops, somethin wrong happened!')

    out = {
        'status': status
    }
    return jsonify(out)

@example1.route("/read_progress_value/<string:ip_address>", methods=['GET'])
@login_required
def read_progress_value(ip_address):
    # progress_bar_value = session.get('progress_bar_value')
    progress_bar_value = cache.get('progress_bar_value_' + ip_address)
    progress_value = progress_bar_value
    time.sleep(CONFIG_TIME_SIM_SPEED)
    out = {
        'progress_value':progress_value
    }
    return jsonify(out)

@example1.route("/verify/<string:ip_board>", methods=['POST'])
@login_required
def verify(ip_board):
    f = request.files.get('file')
    original_data = f.read().decode('utf-8')
    ip_address = request.remote_addr
    if len(ip_address) == 0:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR']
    remote_port = request.environ.get('REMOTE_PORT')
    error = None
    status = 'fail'

    print('Verifying..')

    crc, data_len = calculate_checksum(original_data)
    crc_in_bytes = unhexlify(crc)
    crc_in_str = (convertByte2Str(crc_in_bytes))

    addr = '9d000010'
    size = "%x" % (data_len)
    addr, size = addr.zfill(8), size.zfill(8)
    str_addr = convertByte2Str(unhexlify(addr)[::-1])
    str_size = convertByte2Str(unhexlify(size)[::-1])

    conn_stream = UDPStream(ip_board, 6234, 15)  # 15s timeout
    conn_stream.send_request(CMD_VERIFY_CS + str_addr + str_size + crc_in_str)
    checksum = conn_stream.read_response('\04')
    checksum_pic_calculated = convertByte2Str(checksum)
    print('CRC @%s[%s]: %s' % (addr, size, hexlify(checksum)))

    if checksum_pic_calculated == crc_in_str:
        status = 'success'

    out = {
        'status': status,
        'error': error
    }
    return jsonify(out)
@example1.route("/upload_file/<string:ip_board>", methods=['POST'])
@login_required
def upload_file(ip_board):
    f = request.files.get('file')
    original_data = f.read().decode('utf-8')
    ip_address = request.remote_addr
    if len(ip_address) == 0:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR']
    remote_port = request.environ.get('REMOTE_PORT')
    error = None
    try:
        conn_stream = UDPStream(ip_board, 6234, 15)  # 5s timeout   #pic32mx eth sk

        upstats = upload_data(ip_address, conn_stream, original_data)
        print('Transmitted: %d packets (%d bytes), Received: %d packets (%d bytes)' % (
        upstats[0], upstats[1], upstats[2], upstats[3]))

        # # upload file to board start here
        # #simulating...
        # v = 0
        # while v < 100:
        #     v = v + 5
        #     progress_bar_value = str(v)
        #     cache.set('progress_bar_value_' + ip_address, progress_bar_value)
        #     print("Progress value: %s" % (progress_bar_value))
        #     time.sleep(CONFIG_TIME_SIM_SPEED)
    except Exception as err:
        error = "Hex file uploaded to board has problem"
        print(error)
    time.sleep(1)
    cache.delete('progress_bar_value_' + ip_address)
    out = {
        'status':'success',
        'error':error
    }
    return jsonify(out)

@example1.route("/example1_home", methods=['GET'])
@login_required
def example1_home():
    ip_address = request.remote_addr
    if len(ip_address) == 0:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR']
    remote_port = request.environ.get('REMOTE_PORT')
    form = UpdateFileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            v = 0
            while v < 100:
                v = v + 5
                progress_bar_value = str(v) + '%'
                cache.set('progress_bar_value_' + ip_address,progress_bar_value)
                print("Progress value: %s" %(progress_bar_value))
                time.sleep(CONFIG_TIME_SIM_SPEED)
            E = 1
            status_fw = "Firmware programmed successfully"
            disabled = ""
            cache.delete('progress_bar_value_' + ip_address)

            # return redirect(url_for('example1.example1_home'))
            # return redirect(request.url)

        else:
            v = 0
            progress_bar_value = str(v) + '%'
            status_fw = 'Please upload valid hex file'
    else:
        # random_hex = secrets.token_hex(8)
        v = 0
        progress_bar_value = str(v) + '%'
        status_fw = 'Please enter valid board ip address'
        cache.set('progress_bar_value_%s:%d' %(ip_address,remote_port),progress_bar_value)


        # form.program.render_kw['disabled'] = False
    return render_template('example1.html',
                           title='Example1',
                           form=form,
                           progress_bar_value=progress_bar_value,
                           ip_address=ip_address,
                           status_fw=status_fw,
                           # disabled_=disabled,
                           )

@example1.route("/check_version/<string:ip_addr>", methods=['GET'])
@example1.route("/connect/<string:ip_addr>", methods=['GET'])
@login_required
def connect(ip_addr):
    try:
        conn_stream = UDPStream(ip_addr, 6234, 15)  # 5s timeout

        print('Querying version..')
        conn_stream.send_request(CMD_READ_VERSION)
        version = conn_stream.read_response('\x01')
        print('Bootloader version: ' + hexlify(version).decode())
        s = 'success'
        v = hexlify(version).decode()
    except Exception as err:
        s = 'fail'
        v = None

    out = {
        'status': s,
        'version': v,
    }
    return jsonify(out)

@example1.route("/erase_flash/<string:ip_addr>", methods=['GET'])
@login_required
def erase_flash(ip_addr):

    try:
        conn_stream = UDPStream(ip_addr, 6234, 15)  # 5s timeout   #pic32mx eth sk
        print('Cmd Erase..')
        conn_stream.send_request(CMD_ERASE)
        r = conn_stream.read_response('\x02')
        v = hexlify(r).decode()
    except Exception as err:
        s = 'fail'
        v = ''

    if v == '02':
        s = 'success'
    else:
        s = 'fail'
    o = {
        'status':s,

    }
    return jsonify(o)


