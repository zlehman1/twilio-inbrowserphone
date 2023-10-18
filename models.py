from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UrlModel(db.Model):
	__tablename__ = "urltable"
	
	id = db.Column(db.Integer, primary_key=True)
	recording_url = db.Column(db.String())
	
	def __init__(self, id, url):
		self.id = id
		self.url = url

	def __repr__(self):
		return f"{self.id}:{self.url}"
