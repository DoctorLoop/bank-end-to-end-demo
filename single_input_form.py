from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class InputPredictionForm(FlaskForm):

    age = IntegerField('Age', validators=[DataRequired()])
    job = SelectField('Job', validators=[DataRequired()], choices=[ 'admin','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown'])
    marital = SelectField('Marital', validators=[DataRequired()], choices=['divorced','married','single','unknown'])
    education= SelectField('Education', validators=[DataRequired()], choices=[ 'basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown'])
    default= SelectField('Default', validators=[DataRequired()], choices=[ 'no','yes','unknown'])
    balance=IntegerField('Balance', validators=[DataRequired()])
    housing= SelectField('Housing', validators=[DataRequired()], choices=[ 'no','yes','unknown'])
    loan= SelectField('Loan', validators=[DataRequired()], choices=['no','yes','unknown'])
    contact= SelectField('Contact', validators=[DataRequired()], choices=['cellular','telephone'])
    day=IntegerField('Day', validators=[DataRequired()])
    month= SelectField('Month', validators=[DataRequired()], choices=['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
    duration=IntegerField('Duration')
    campaign=IntegerField('Campaign', validators=[DataRequired()])
    pdays=IntegerField('PDays', validators=[DataRequired()])
    previous=IntegerField('Previous', validators=[DataRequired()])
    poutcome= SelectField('POutcome', validators=[DataRequired()], choices=['failure','nonexistent','success'])

    submit = SubmitField('Predict Subscription', id="predict-submit")

