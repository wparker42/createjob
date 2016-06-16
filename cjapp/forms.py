from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField, RadioField
from wtforms import validators as val

class JobForm(Form):
    jobname = TextField('Search',
                        validators=[val.Required(),
                                    val.Length(min=3, max=128)])
