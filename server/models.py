"""
models.py
- Data classes for the surveyapi application

datetime_format = "%Y-%m-%d %H:%M:%S"
date_time_str = datetime.utcnow().strftime(datetime_format) 
date_time_obj = datetime.strptime(date_time_str, datetime_format)
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

########################################
class User:
    def __init__(self, userId=0, email=None, password=None, firstname=None, lastname=None, dob=None, gender=None, image=None):
        self.userId = userId
        self.email = email
        self.password = generate_password_hash(password, method='sha256') if password else None
        self.firstname = firstname
        self.lastname = lastname        
        self.dob = dob
        self.gender = gender
        self.image = image

    def to_dict(self):
      return dict(userId=self.userId,
                  email=self.email,
                  password=self.password,
                  firstname=self.firstname,
                  lastname=self.lastname,
                  dob=self.dob,
                  gender=self.gender,
                  image=self.image)

    @staticmethod
    def authenticate(source, target):
        return check_password_hash(source, target)

class BPStat:
    def __init(self, bpStatId=0, userId=0, sys=0, dia=0, position=None, activity=None, notes=None, recordDateTime=datetime.utcnow()):
        self.bpStatId = bpStatId
        self.userId = userId
        self.sys = sys
        self.dia = dia
        self.position = position
        self.activity = activity
        self.notes = notes
        self.recordDateTime = recordDateTime.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
      return dict( bpStatId = self.bpStatId,
                   userId = self.userId,
                   sys = self.sys,
                   dia = self.dia,
                   position = self.position,
                   activity = self.activity,
                   notes = self.notes,
                   recordDateTime = self.recordDateTime)
                  #created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                  #questions=[question.to_dict() for question in self.questions])

class Pulse:
    def __init(self, pulseId=0, userId=0, pulse=0, activity=None, notes=None, recordDateTime=datetime.utcnow()):
        self.pulseId = pulseId
        self.userId = userId
        self.pulse = pulse
        self.activity = activity
        self.notes = notes
        self.recordDateTime = recordDateTime.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
      return dict( pulseId = self.pulseId,
                   userId = self.userId,
                   pulse = self.pulse,
                   activity = self.activity,
                   notes = self.notes,
                   recordDateTime = self.recordDateTime) 

class Weight:
    def __init(self, weightId=0, userId=0, weight=0, notes=None, recordDateTime=datetime.utcnow()):
        self.weightId = weightId
        self.userId = userId
        self.weight = weight
        self.notes = notes
        self.recordDateTime = recordDateTime.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
      return dict( weightId = self.weightId,
                   userId = self.userId,
                   weight = self.weight,
                   notes = self.notes,
                   recordDateTime = self.recordDateTime)                    