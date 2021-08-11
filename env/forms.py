from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField,validators,SelectField
from wtforms.fields.core import IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import Email, InputRequired, Length, ValidationError, DataRequired, EqualTo
from models import Login,NewPatient
class RegistrationForm(FlaskForm):
        username= StringField('Username',validators=[DataRequired(), Length(min=5,max=20)], render_kw={'placeholder':'Username'})
        password= PasswordField('Password',validators=[DataRequired(), Length(min=5,max=20)], render_kw={'placeholder':'Password'})
        confirm_password =PasswordField('Confirm_password', validators=[DataRequired(),EqualTo('password')],render_kw={'placeholder':'Confirm Password'})
        submit= SubmitField('Register')

class LoginForm(FlaskForm):
        username= StringField('Username',validators=[DataRequired(), Length(min=5,max=20)], render_kw={'placeholder':'Username'})
        password= PasswordField('Password',validators=[DataRequired(), Length(min=5,max=20)], render_kw={'placeholder':'Password'})
        remember = BooleanField('Remember Me')
        submit= SubmitField('Register')

class NewPatientP(FlaskForm):
        patient_id= StringField('Patient_Id',validators=[DataRequired(), Length(min=5, max=10)], render_kw={'placeholder':'Patient_Id'})
        patient_name=StringField('Patient_Name',validators=[DataRequired(),Length(min=5,max=15)],render_kw={'placeholder':'Patient_name'})
        age= IntegerField('Age',validators=[DataRequired()], render_kw={'placeholder':'Age'})
        sex= StringField('Sex',validators=[DataRequired(), Length(min=1,max=10)], render_kw={'placeholder':'Sex'})
        father_name= StringField('Father_name',validators=[DataRequired(), Length(min=5,max=20)], render_kw={'placeholder':'Father_name'})
        mother_name= StringField('Mother_name',validators=[DataRequired(), Length(min=5,max=20)], render_kw={'placeholder':'Mother_name'})
        dob= DateField('DOB',validators=[DataRequired()], render_kw={'placeholder':'DOB'})
        patient_contact= IntegerField('Patient_contact',validators=[DataRequired()], render_kw={'placeholder':'Patient_contact'})
        parent_contact= IntegerField('Parent_contact',validators=[DataRequired()], render_kw={'placeholder':'Parent_contact'})
        address= StringField('Address',validators=[DataRequired(), Length(min=5,max=100)], render_kw={'placeholder':'Address'})
        village_name=StringField('Village_Name',validators=[DataRequired()],render_kw={'placeholder':'Village_Name'})
        occupation= StringField('Occupation',validators=[DataRequired(), Length(min=5,max=100)], render_kw={'placeholder':'Occupation'})
        email_id= StringField('Email_Id',validators=[DataRequired(),Email()],render_kw={'placeholder':'Email'})
        submit= SubmitField('Submit')
        def validate_username(self,patient_id):
            existing_user_username = NewPatient.query.filter_by(patient_id=patient_id.data).first()
            if existing_user_username:
                raise ValidationError(
                    'Patient Exists'                                
                )

class ExistingPatientP(FlaskForm):
    patient_no=IntegerField('Patient_no',validators=[DataRequired()],render_kw={'placeholder':'Patient_no'})
    doctor_id=StringField('Doctor_id',validators=[DataRequired()],render_kw={'placeholder':'Doctor_id'})
    doctor_name=StringField('Doctor_name',render_kw={'placeholder':'Doctor_name'})
    submit=SubmitField('Submit')

class SearchPatient(FlaskForm):
    patient_name=StringField('Patient_Name',validators=[DataRequired()],render_kw={'placeholder':'Patient_Name'})
    patient_age=IntegerField('Patient_Age',validators=[DataRequired()],render_kw={'placeholder':'Patient_Age'})
    father_name=StringField('Father_Name',validators=[DataRequired()],render_kw={'placeholder':'Father_Name'})
    village_name=StringField('Village_Name',validators=[DataRequired()],render_kw={'placeholder':'Village_Name'})
    patient_contact=StringField('Contact_Number',render_kw={'placeholder':'Patient_Contact'})

class PatientVitalsP(FlaskForm):
    patient_id=StringField('Patient_Id',validators=[DataRequired()],render_kw={'placeholder':'Patient_Id'})
    patient_no=IntegerField('Patient_no',validators=[DataRequired()],render_kw={'placeholder':'Patient_no'})
    symptoms=StringField('Symptoms',validators=[DataRequired()],render_kw={'placeholder':'Symptoms'})
    weigth=StringField('Weigth',validators=[DataRequired()],render_kw={'placeholder':'Weight'})
    temperature=StringField('Temperature',validators=[DataRequired()],render_kw={'placeholder':'Temperature'})
    bp=StringField('Blood_pressure',validators=[DataRequired()],render_kw={'placeholder':'Blood_pressure'})
    covidinformation=StringField('Covid_information',validators=[DataRequired()],render_kw={'placeholder':'Had Covid?'})

class PatientHistoryP(FlaskForm):
    history=StringField('History',validators=[DataRequired()],render_kw={'placeholder':'Medical_History'})
    allergy=StringField('Allergy',validators=[DataRequired()],render_kw={'placeholder':'Allergy'})

class Medicines(FlaskForm):
    salt=SelectField('Salt',choices=[])
    brand=SelectField('Brand',choices=[])
    day=IntegerField('Day')
    lunch=IntegerField('Lunch')
    dinner=IntegerField('Dinner')