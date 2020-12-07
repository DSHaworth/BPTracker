"""
models.py
- Data classes for the surveyapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

########################################

class User:
    def __init__(self, userId=0, email=None, firstname=None, lastname=None, password=None, dob=None, image=None):
        self.userId = userId
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.firstname = firstname
        self.lastname = lastname        
        self.image = image
        self.dob = dob

    def to_dict(self):
      return dict(userId=self.userId,
                  email=self.email,
                  password=self.password,
                  firstname=self.firstname,
                  lastname=self.lastname,
                  image=self.image,
                  dob=self.dob)

class BPStat:

    def __init(self, bpStatId=0, userId=0, sys=0, dia=0, pulse=0, bpTaken=None, position=None):
        self.bpStatId = bpStatId
        self.userId = userId
        self.sys = sys
        self.dia = dia
        self.pulse = pulse
        self.bpTaken = bpTaken
        self.position = position

    # def to_dict(self):
    #   return dict(id=self.bpStatId,
    #               name=self.name,
    #               created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    #               questions=[question.to_dict() for question in self.questions])