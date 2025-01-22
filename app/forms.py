from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class VideoSubmitForm(FlaskForm):
    link = StringField('Link to video')
    submit = SubmitField('Analyze')