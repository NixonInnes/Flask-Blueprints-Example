from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ExampleForm(FlaskForm):
    text = StringField('Text: ', default='A default string', validators=[DataRequired(), Length(5)])
    submit = SubmitField()
