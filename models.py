 # from flask_sqlalchemy import SQLAlchemy
 #
 # db = SQLAlchemy()
 #
 # class UrlModel(db.Model):
 #   __tablename__ = "urltable"
 #
 #   id = db.Column(db.Integer, primary_key=True)
 #   recording_url = db.Column(db.String())
 #   recording_duration = db.Column(db.String())
 #
 #   def __init__(self, id, url, duration):
 #      self.id = id
 #      self.url = url
 #      self.duration = duration
 #
 #   def __repr__(self):
 #      return f"{self.id}:{self.url, self.duration}"
 
 from flask_sqlalchemy import SQLAlchemy
 
 db = SQLAlchemy()
 
 
 class UrlModel(db.Model):
     __tablename__ = "urltable"
 
     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     recording_url = db.Column(db.String())
     recording_duration = db.Column(db.String())
     to_number = db.Column(db.String())
 
     def __init__(self, id, recording_url, recording_duration, recording_number):
        self.id = id
        self.recording_url = recording_url
        self.recording_duration = recording_duration
        self.to_number = to_number
 
     def __repr__(self):
        return f"{self.id}:{self.recording_url}, {self.recording_duration}, {self.to_number}"
