from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import TextAreaField, IntegerField
from wtforms.validators import DataRequired

class Compare_sentence_sim(FlaskForm):
    text1 = TextAreaField('Text1', validators=[DataRequired()])
    text2 = TextAreaField('Text2', validators=[DataRequired()])

class Context_file(FlaskForm):
    file = FileField('Context', validators=[FileRequired()])

class Compare_SnF(FlaskForm):
    query = TextAreaField('Query', validators=[DataRequired()])
    number = IntegerField('Number', validators=[DataRequired()])
