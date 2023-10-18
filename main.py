from flask import Flask, render_template, jsonify
from flask import request, Response, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
 
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
 
from dotenv import load_dotenv
import os
import pprint as p

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
api_key = os.getenv('TWILIO_API_KEY_SID')
api_key_secret = os.getenv('TWILIO_API_KEY_SECRET')
twiml_app_sid = os.getenv('TWIML_APP_SID')
twilio_number = os.getenv('TWILIO_NUMBER')

app = Flask(__name__)

# Configure your SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///urlcollection.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SQLAlchemy database object
db = SQLAlchemy(app)

# Define your database model (TestModel in this case)
class UrlModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recording_url = db.Column(db.String(255))

# Define a function to create the tables
def create_tables():
    with app.app_context():
        db.create_all()

# Create a database if it doesn't exist
create_tables()

# Render the home page when we take up the application
@app.route('/')
def home():
    return render_template(
        'home.html',
        title="In browser calls",
    )

# Get the access token to actually use the phone feature
@app.route('/token', methods=['GET'])
def get_token():
    identity = twilio_number
    outgoing_application_sid = twiml_app_sid

    access_token = AccessToken(account_sid, api_key,
                               api_key_secret, identity=identity)

    voice_grant = VoiceGrant(
        outgoing_application_sid=outgoing_application_sid,
        incoming_allow=True,
    )
    access_token.add_grant(voice_grant)

    response = jsonify(
        {'token': access_token.to_jwt(), 'identity': identity})

    return response

@app.route('/handle_calls', methods=['POST'])
def call():
    p.pprint(request.form)
    response = VoiceResponse()
    dial = Dial(
	callerId=twilio_number,
	record='record-from-answer',
	recording_status_callback='/recording_callback'
	)

    if 'To' in request.form and request.form['To'] != twilio_number:
        print('outbound call')
        dial.number(request.form['To'])
    else:
        print('incoming call')
        caller = request.form['Caller']
        dial = Dial(callerId=caller)
        dial.client(twilio_number)

    return str(response.append(dial))

recording_url = None

@app.route('/recording_callback', methods=['GET', 'POST'])
def record():
    # Get the parameters from Twilio recording
    account_sid = request.form['AccountSid'] 		
    call_sid = request.form['CallSid'] 
    recording_sid = request.form['RecordingSid'] 
    recording_url = request.form['RecordingUrl'] 
    recording_status = request.form['RecordingStatus'] 
    recording_duration = request.form['RecordingDuration'] 
    recording_channels = request.form['RecordingChannels'] 
    recording_start_time = request.form['RecordingStartTime'] 
    recording_source = request.form['RecordingSource']
    response_text = f"Account SID: {account_sid}\nCall SID: {call_sid}\nRecording SID: {recording_sid}\nRecording URL: {recording_url}\nRecording Status: {recording_status}\nRecording Duration: {recording_duration}\nRecording Channels: {recording_channels}\nRecording Start Time: {recording_start_time}\nRecording Source: {recording_source}"
	
    print(response_text)

    url_list = UrlModel(recording_url=recording_url)
    db.session.add(url_list)
    db.session.commit()

    return redirect('/urldata')

@app.route('/urldata')
def retrieve_url_data():
    urllists = UrlModel.query.all()
    return render_template('urldata.html', urllists=urllists)    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
