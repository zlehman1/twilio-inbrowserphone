from flask import Flask, render_template, jsonify
from flask import request, Response, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial

from dotenv import load_dotenv
import os
import pprint as p

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
api_key = os.getenv('TWILIO_API_KEY')
api_key_secret = os.getenv('TWILIO_API_SECRET')
twiml_app_sid = os.getenv('TWILIO_APP_SID')
twilio_number = os.getenv('TWILIO_NUMBER')

app = Flask(__name__)

# Configure your SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///urlcollection.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SQLAlchemy database object
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define your database model (TestModel in this case)
class UrlModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recording_url = db.Column(db.String(255))
    recording_duration = db.Column(db.String(20))
    to_number = db.Column(db.String(20))


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
    try:
        identity = twilio_number
        outgoing_application_sid = twiml_app_sid

        access_token = AccessToken(account_sid, os.getenv('TWILIO_API_KEY'),
                                   os.getenv('TWILIO_API_SECRET'), identity=identity)

        voice_grant = VoiceGrant(
            outgoing_application_sid=outgoing_application_sid,
            incoming_allow=True,
        )
        access_token.add_grant(voice_grant)

        response = jsonify(
            {'token': access_token.to_jwt().decode('utf-8'), 'identity': identity}
        )

        return response
    except Exception as e:
        print(f"Error generating token: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to generate token', 'details': str(e)}), 500

to_number = None

@app.route('/handle_calls', methods=['POST'])
def call():
    global to_number
    p.pprint(request.form)
    response = VoiceResponse()
    dial = Dial(
        callerId=twilio_number,
        # callerId="+916282543120",
        record='record-from-answer',
        recording_status_callback='/recording_callback'
    )


    if 'To' in request.form and request.form['To'] != twilio_number:
        print('outbound call')
        to_number = (request.form['To'])
        print("Inside the function", to_number)
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

    print("Inside record function", to_number)
    print(response_text)

    # recording_id = int(UrlModel(id=id))
    # url_list = UrlModel(recording_url=recording_url)
    # recording_duration = UrlModel(recording_duration=recording_duration)

    new_record = UrlModel(recording_url=recording_url, recording_duration=recording_duration, to_number=to_number)

    db.session.add(new_record)
    db.session.commit()

    return redirect('/urldata')


@app.route('/urldata')
def retrieve_url_data():
    urllists = UrlModel.query.all()
    return render_template('urldata.html', urllists=urllists)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
