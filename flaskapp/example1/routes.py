import secrets
import time
from flask_login import current_user, login_required
from flask import render_template, Blueprint, redirect, url_for, session, jsonify, request
from flaskapp.example1.form import UpdateFileForm
from flaskapp import cache


example1 = Blueprint('example1', __name__)
CONFIG_TIME_SIM_SPEED = 0.5

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
#   return "Progress value: " + str(progress_value)

@example1.route("/example1_home", methods=['GET', 'POST'])
@login_required
def example1_home():
    ip_address = request.remote_addr
    if len(ip_address) == 0:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR']
    remote_port = request.environ.get('REMOTE_PORT')
    form = UpdateFileForm()
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
        cache.delete('progress_bar_value_' + ip_address)
        # return redirect(url_for('example1.example1_home'))
    else:
        # random_hex = secrets.token_hex(8)
        v = 0
        progress_bar_value = str(v) + '%'
        cache.set('progress_bar_value_%s:%d' %(ip_address,remote_port),progress_bar_value)
        status_fw = 'Ready'

        # form.program.render_kw['disabled'] = False
    return render_template('example1.html',
                           title='Example1',
                           form=form,
                           progress_bar_value=progress_bar_value,
                           ip_address=ip_address,
                           status_fw=status_fw,
                           )

@example1.route("/check_version", methods=['GET'])
def check_version():
    return render_template('example1.html', title='Example1')

@example1.route("/verify", methods=['GET'])
def verify():
    return render_template('example1.html', title='Example1')