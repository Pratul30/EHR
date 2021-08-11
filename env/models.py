from datetime import datetime
from env import db,login_manager
from flask_login import UserMixin

class Login(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    login_id= db.Column(db.String(100),nullable=False)
    password_id = db.Column(db.String(100),nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)


class NewPatient(db.Model,UserMixin):
    __tablename__='newpatient'
    id = db.Column(db.Integer,primary_key=True)
    patient_id= db.Column(db.String(10),nullable=False)
    patient_name=db.Column(db.String(15),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    sex= db.Column(db.String(10),nullable=False)
    father_name=db.Column(db.String(100),nullable=False)
    mother_name= db.Column(db.String(100),nullable=False)
    dob=db.Column(db.DateTime,nullable=False)
    patient_contact= db.Column(db.Integer,nullable=False)
    parent_contact=db.Column(db.Integer,nullable=False)
    address= db.Column(db.String(100),nullable=False)
    village_name=db.Column(db.String(10),nullable=False)
    occupation=db.Column(db.String(100),nullable=False)
    email_id= db.Column(db.String(10),nullable=False)
    parent=db.relationship('ExistingPatient',backref='owner')
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

class ExistingPatient(db.Model,UserMixin):
    __tablename__='existingpatient'
    id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.Integer,nullable=False)
    patient_no=db.Column(db.Integer,nullable=False)
    doctor_id=db.Column(db.String(10))
    doctor_name=db.Column(db.String(50),nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.now())
    owner_id=db.Column(db.Integer,db.ForeignKey('newpatient.id'))

class PatientVitals(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.String(10),nullable=False)
    patient_no=db.Column(db.Integer,nullable=False)
    weigth=db.Column(db.String(5))
    temperature=db.Column(db.String(5),nullable=False)
    bp=db.Column(db.String(5))
    date_time = db.Column(db.DateTime, default=datetime.now())

class PatientHistory(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.String(10),nullable=False)
    patient_no=db.Column(db.Integer,nullable=False)
    history=db.Column(db.String(100))
    allergy=db.Column(db.String(100))
    symptoms=db.Column(db.String(50))
    covidinformation=db.Column(db.String(10),nullable=False)

class PatientMedicines(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.String(10),nullable=False)
    salt=db.Column(db.String(20),nullable=False)
    brand=db.Column(db.String(20),nullable=False)
    day=db.Column(db.Integer,nullable=False)
    lunch=db.Column(db.Integer,nullable=False)
    dinner=db.Column(db.Integer,nullable=False)
    doctor_id=db.Column(db.String(10),nullable=False)

class Doctor(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    doctor_id=db.Column(db.String(10))
    first_name=db.Column(db.String(10))
    surname=db.Column(db.String(10))
    speciality=db.Column(db.String(20))
    designation=db.Column(db.String(20))
    specialization=db.Column(db.String(50))

class MedicinesModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    salt=db.Column(db.String(20))
    strength=db.Column(db.String(10))
    type=db.Column(db.String(10))
    associated_medicine=db.Column(db.String(20))
    brand=db.Column(db.String(20))
    