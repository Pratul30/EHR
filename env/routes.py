from operator import and_
from flask import *
from flask.sessions import NullSession
from flask_sqlalchemy import model
from sqlalchemy.orm import selectin_polymorphic
from werkzeug.local import F
from wtforms.widgets.core import Select
from env import app,db,bcrypt,login_manager
from forms import RegistrationForm,LoginForm,NewPatientP,ExistingPatientP,SearchPatient,PatientVitalsP,PatientHistoryP,Medicines
from models import Login,NewPatient,ExistingPatient,Doctor,PatientVitals,PatientHistory,MedicinesModel,PatientMedicines
from flask_login import login_user,current_user,logout_user,login_required
from datetime import date, datetime,timedelta
from wtforms.validators import ValidationError
import pandas as pd
import csv
import flask_excel as excel
import io


@app.route('/', methods=['GET','POST'])
def hello_world(): 
    return render_template('authority.html')
    #return 'Hello, World!'

@app.route('/register',methods=['GET','POST'])
def registerreceptionist():
    registerform=RegistrationForm()
    if request.method=='POST':
        username= request.form['username']
        exist_username=Login.query.filter_by(login_id=username).first()
        if exist_username:
            flash('Login_id Exists','danger')
            return render_template('receptionistregister.html',form=registerform)
        if registerform.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(registerform.password.data).decode('utf-8')
            new_user=Login(login_id=registerform.username.data,password_id=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    return render_template('receptionistregister.html',form=registerform)


@app.route('/authority')
def authorithy():
    return render_template('authority.html')

@app.route('/patientmethod')
def patientmethod():
    if current_user.is_authenticated:
        return render_template('patientmethod.html',user=current_user)
    else:
        return 'hi'

@app.route('/pratul')
def pratul():
    time_create=request.cookies.get('time_create')
    time_date=datetime.strptime(time_create,'%Y-%m-%d %H:%M:%S.%f')
    patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date),(ExistingPatient.doctor_id)==(Login.login_id)))
    print(patient)
    return render_template('pratul.html',patient=patient)

@login_manager.user_loader
def load_user1(login_receptionist_id):
    return (Login.query.get(int(login_receptionist_id)))


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    sno=request.cookies.get('sno')
    if request.method=='POST':
        user = Login.query.filter_by(login_id=form.username.data).first()
        if form.validate_on_submit():
            if user.login_id=='12345' and bcrypt.check_password_hash(user.password_id,form.password.data):
                login_user(user)
                print('hi')
                return redirect(url_for('patientmethod'))
            else:
                flash('Wrong Username or Password','danger')
        if form.validate_on_submit():
            if user.login_id=='1234512345' and bcrypt.check_password_hash(user.password_id     ,form.password.data):
                time_create_staff=str(datetime.now())
                time_date1=datetime.strptime(time_create_staff,'%Y-%m-%d %H:%M:%S.%f')
                patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date1),(ExistingPatient.doctor_id==user.login_id)))   
                res=make_response(redirect('/appointedstaff'))
                res.set_cookie('time_create_staff',str(datetime.now()))
                temp=False 
                print('login')
                login_user(user)
                return res  
        if form.validate_on_submit():
            if user.login_id=='p1234512345' and bcrypt.check_password_hash(user.password_id     ,form.password.data):
                login_user(user)
                time_create=str(datetime.now())
                time_date=datetime.strptime(time_create,'%Y-%m-%d %H:%M:%S.%f')
                patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date),(ExistingPatient.doctor_id==user.login_id)))   
                res=make_response(redirect('/pratul'))
                res.set_cookie('time_create',str(datetime.now()))
                res.set_cookie('doctor_id',user.login_id)
                temp=False 
                print('login')
                return res
    return render_template('login.html',form=form)

@app.route('/searchpatient',methods=['GET','POST'])
def searchpatient():
    form=SearchPatient()
    if request.method=='POST':
        patient_name=request.form['patient_name']
        patient_age=request.form['patient_age']
        father_name=request.form['father_name']
        village_name=request.form['village_name']
        patient_contact=request.form['patient_contact']
        patientresult=NewPatient.query.filter((NewPatient.patient_name==patient_name)|(NewPatient.age==patient_age)|(NewPatient.father_name==father_name)|(NewPatient.village_name==village_name)|(NewPatient.patient_contact==patient_contact))
        return render_template('searchpatient.html',form=form,patientresult=patientresult)
    return render_template('searchpatient.html',form=form)

@app.route('/logindoctor',methods=['GET','POST'])
def logindoctor():
    form=LoginForm()
    session.permanent=True
    app.permanent_session_lifetime=timedelta(hours=12)
    if form.validate_on_submit():
        user = Login.query.filter_by(login_id=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_id     ,form.password.data):
            login_user(user)
            time_create=str(datetime.now())
            time_date=datetime.strptime(time_create,'%Y-%m-%d %H:%M:%S.%f')
            patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date),(ExistingPatient.doctor_id==user.login_id)))   
            res=make_response(render_template('pratul.html',user=user,patient=patient,yes=True))
            res.set_cookie('time_create',str(datetime.now()))
            temp=False 
            print('login')
            return res
        if current_user.is_authenticated:
            time_create=request.cookies.get('time_create')
            time_date=datetime.strptime(time_create,'%Y-%m-%d %H:%M:%S.%f')
            patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date),(ExistingPatient.doctor_id)==(Login.login_id))).first() 
            print(patient.owner.patient_name) 
            return render_template('pratul.html',patient=patient,yes=True)
    return render_template('doctorlogin.html',form=form)


@app.route('/patientid/<string:patient_id>',methods=['GET','POST'])
def patientid(patient_id):
    time_create=request.cookies.get('time_create')
    time_date=datetime.strptime(time_create,'%Y-%m-%d %H:%M:%S.%f')
    patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date),(ExistingPatient.doctor_id)==(Login.login_id)))   
    newpatient=NewPatient.query.filter_by(patient_id=patient_id)
    res=make_response(render_template('pratul.html',patient=patient,tab=1,newpatient=newpatient))
    res.set_cookie('patient_id',patient_id)
    return res

@app.route('/patientprofile',methods=['GET','POST'])
def patientprofile():
    time_create=request.cookies.get('time_create')
    time_date=datetime.strptime(time_create,'%Y-%m-%d %H:%M:%S.%f')
    patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date),(ExistingPatient.doctor_id)==(Login.login_id)))
    patient_id=request.cookies.get('patient_id')   
    newpatient=NewPatient.query.filter_by(patient_id=patient_id)
    return render_template('pratul.html',patient=patient,tab=1,newpatient=newpatient)

@app.route('/clinicalevaluation',methods=['GET','POST'])
def clinicalevaluation():
    time_create=request.cookies.get('time_create')
    time_date=datetime.strptime(time_create,'%Y-%m-%d %H:%M:%S.%f')
    patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date),(ExistingPatient.doctor_id)==(Login.login_id))) 
    patient_id=request.cookies.get('patient_id')
    vitalspatient=PatientVitals.query.filter_by(patient_id=patient_id)
    return render_template('pratul.html',patient=patient,tab=2,vitalspatient=vitalspatient)
@app.route('/medicines',methods=['GET','POST'])
def medicines():
    time_create=request.cookies.get('time_create')
    time_date=datetime.strptime(time_create,'%Y-%m-%d %H:%M:%S.%f')
    patient=ExistingPatient.query.filter(and_((ExistingPatient.date_time)>(time_date),(ExistingPatient.doctor_id)==(Login.login_id))) 
    patient_id=request.cookies.get('patient_id')
    form=Medicines()
    form.salt.choices=[(salt.salt,salt.salt) for salt in MedicinesModel.query.with_entities(MedicinesModel.salt).distinct()]
    form.brand.choices=[(brand.id,brand.brand) for brand in MedicinesModel.query.all()]
    medicines=MedicinesModel.query.all()
    if request.method=='POST':
        salt=request.form['salt']
        brand=request.form['brand']
        day=request.form['day']
        lunch=request.form['lunch']
        dinner=request.form['dinner']
        patientmedicine=PatientMedicines(patient_id=patient_id,salt=salt,brand=brand,day=day,lunch=lunch,dinner=dinner,doctor_id=request.cookies.get('doctor_id'))
        db.session.add(patientmedicine)
        db.session.commit()
    return render_template('pratul.html',patient=patient,tab=3,medicines=medicines,form=form)
@app.route('/patientmedicines/<salt>')
def patientmedicines(salt):
    brands=MedicinesModel.query.filter_by(salt=salt).all()
    brandArray=[]
    for brand in brands:
        brandObj={}
        brandObj['id']=brand.id
        brandObj['brand']=brand.brand
        brandObj['strength']=brand.strength
        brandObj['type']=brand.type
        brandObj['am']=brand.associated_medicine
        brandArray.append(brandObj)
    return jsonify({'brands':brandArray})


@app.route('/newpatient',methods=['GET','POST'])
def patient():
    newpatientform=NewPatientP()
    if request.method=='POST':
        if newpatientform.validate_on_submit():
            patient_id=request.form['patient_id']
            patient_name=request.form['patient_name']
            age=request.form.get('age',type=int)
            sex=request.form['sex']
            father_name=request.form['father_name']
            mother_name=request.form['mother_name']
            p =newpatientform.dob.data
            dob=p 
            patient_contact=request.form.get('patient_contact',type=int)
            parent_contact=request.form.get('parent_contact',type=int)
            address=request.form['address']
            village_name=request.form['village_name']
            occupation=request.form['occupation']
            email_id=request.form['email_id']
            newpatient=NewPatient(patient_id=patient_id,patient_name=patient_name,age=age,sex=sex,father_name=father_name,mother_name=mother_name,dob=dob,patient_contact=patient_contact,parent_contact=parent_contact,address=address,village_name=village_name,occupation=occupation,email_id=email_id)
            db.session.add(newpatient)
            db.session.commit()
            return render_template('patientmethod.html')
    return render_template('newpatient.html',newpatientform=newpatientform)

@app.route('/existingpatient',methods=['GET','POST'])
def existingpatient():
    form=ExistingPatientP()
    form1=NewPatientP()
    doctor=Doctor.query.all()
    if request.method=='POST':
        if form.validate_on_submit():
            patient_id=request.form['patient_id']
            patient_no=request.form['patient_no']
            doctor_id=request.form['doctor_id']
            newpatient=NewPatient.query.filter_by(patient_id=patient_id).first()
            if newpatient:
                existingpatient=ExistingPatient(patient_id=patient_id,patient_no=patient_no,doctor_id=doctor_id,doctor_name='12345',date_time=datetime.now(),owner=newpatient)
                db.session.add(existingpatient)
                db.session.commit()
                flash('Patient Appointment Booked', 'success')
                return render_template('patientmethod.html')
            else:
                flash('Patient Does Not Exist','danger')
                return render_template('existingpatient.html',form=form,form1=form1) 
    else:
        print('pratul')   
    return render_template('existingpatient.html',form=form,form1=form1,doctor=doctor)

@app.route('/loginstaff',methods=['GET','POST'])
def loginstaff():
   # if current_user.is_authenticated:
    #return redirect('/login')
    form=LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(login_id=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_id     ,form.password.data):
            login_user(user,remember=True)
            return redirect('/staffpatient')
    two_id=Login.query.all()
    return render_template('stafflogin.html',two_id=two_id,form=form)

@app.route('/appointedstaff')
@login_required
def appointedstaff():
    time_create_staff=request.cookies.get('time_create_staff')
    time_date=datetime.strptime(time_create_staff,'%Y-%m-%d %H:%M:%S.%f')
    patient=ExistingPatient.query.filter(ExistingPatient.date_time>time_date)
    patient_no=ExistingPatient.query.filter(ExistingPatient.date_time>time_date).order_by(ExistingPatient.id.desc()).first()
    return render_template('appointedstaff.html',patient=patient,patient_no=patient_no)

@app.route('/staffpatient/<string:patient_id>',methods=['GET','POST'])
@login_required
def staffpatient(patient_id):
    form=PatientVitalsP()
    form1=PatientHistoryP()
    patient=ExistingPatient.query.filter_by(patient_id=patient_id).first()
    if request.method=='POST':
        symptoms=request.form['symptoms']
        weigth=request.form['weigth']
        temperature=request.form['temperature']
        bp=request.form['bp']
        covidinformation=request.form['covidinformation']
        history=request.form['history']
        allergy=request.form['allergy']
        patientvitals=PatientVitals(patient_id=patient.patient_id,patient_no=patient.patient_no,weigth=weigth,temperature=temperature,bp=bp)
        patienthistory=PatientHistory(patient_id=patient.patient_id,patient_no=patient.patient_no,history=history,allergy=allergy,symptoms=symptoms,covidinformation=covidinformation)
        db.session.add(patientvitals)
        db.session.add(patienthistory)
        db.session.commit()
        return redirect('/appointedstaff')
    return render_template('staffpatient.html',form=form,form1=form1,user=current_user,patient=patient)

@app.route('/doctor',methods=['GET','POST'])
def doctor():
    if request.method=='POST':
        file=request.files['pratulhtml']
        filestream = io.StringIO(file.stream.read().decode('UTF8'),newline=None)
        fileinput=csv.reader(filestream)
        print(fileinput)
        for row in fileinput:
            newrow=MedicinesModel(salt=row[0],strength=row[1],type=row[2],associated_medicine=row[3],brand=row[4])
            db.session.add(newrow)
            db.session.commit()
    return render_template('excel.html')

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        login_id= request.form['login_id']
        password_id= request.form['password_id']
        test= Login.query.filter_by(id=id).first()
        test.login_id=login_id
        test.password_id=password_id
        db.session.add(test)
        db.session.commit()
        return redirect('/')
    two_id= Login.query.filter_by(id=id).first()
    return render_template('update.html',two_id=two_id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')  