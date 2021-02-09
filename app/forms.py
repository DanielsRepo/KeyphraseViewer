from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ViewerForm(FlaskForm):
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Get keyphrases")
