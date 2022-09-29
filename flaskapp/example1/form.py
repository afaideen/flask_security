
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class UpdateFileForm(FlaskForm):
    hexfile = FileField('Load hex file', validators=[FileAllowed(['hex'])],
                        render_kw={
                            'oninput':'enableProgramButton()',
                            'accept':'.hex'
                        })
    # program = SubmitField('Program',  render_kw={'disabled': 'disabled'})
    program = SubmitField('Program')