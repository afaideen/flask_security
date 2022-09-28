
from flask import render_template, Blueprint
from flaskapp.example1.form import UpdateFileForm

example1 = Blueprint('example1', __name__)

@example1.route("/example1_home", methods=['GET', 'POST'])
def example1_home():
    form = UpdateFileForm()
    if form.validate_on_submit():
        pass
    else:
        pass
        # form.program.render_kw['disabled'] = False
    return render_template('example1.html', title='Example1', form=form)

@example1.route("/check_version", methods=['GET'])
def check_version():
    return render_template('example1.html', title='Example1')

@example1.route("/verify", methods=['GET'])
def verify():
    return render_template('example1.html', title='Example1')