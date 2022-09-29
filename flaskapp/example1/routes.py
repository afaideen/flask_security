
from flask import render_template, Blueprint, redirect, url_for
from flaskapp.example1.form import UpdateFileForm

example1 = Blueprint('example1', __name__)

@example1.route("/example1_home", methods=['GET', 'POST'])
def example1_home():
    form = UpdateFileForm()
    if form.validate_on_submit():
        progress_bar_value = '75%'

        # return redirect(url_for('example1.example1_home'))
    else:
        progress_bar_value = '5%'
        # form.program.render_kw['disabled'] = False
    return render_template('example1.html', title='Example1', form=form, progress_bar_value=progress_bar_value)

@example1.route("/check_version", methods=['GET'])
def check_version():
    return render_template('example1.html', title='Example1')

@example1.route("/verify", methods=['GET'])
def verify():
    return render_template('example1.html', title='Example1')