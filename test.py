from flask import Flask, render_template, jsonify
from flask import request
 
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

test = Flask(__name__)

# Render the home page when we take up the application
@test.route('/')
def home():
    return render_template(
        'home.html',
        title="In browser calls",
    )

# Get the access token to actually use the phone feature
@test.route('/token', methods=['GET'])
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

@test.route('/handle_calls', methods=['POST'])
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

# Recording
@test.route('/recording_callback', methods=['POST'])
def record():
    # Get the parameters from the request
    account_sid = request.form['AccountSid']
    call_sid = request.form['CallSid']
    recording_sid = request.form['RecordingSid']
    recording_url = request.form['RecordingUrl']
    recording_status = request.form['RecordingStatus']
    recording_duration = request.form['RecordingDuration']
    recording_channels = request.form['RecordingChannels']
    recording_start_time = request.form['RecordingStartTime']
    recording_source = request.form['RecordingSource']

    # Process and store the recording as needed
    # You can use these parameters for further actions like storing the recording URL, duration, etc.

    # For example, you can print these values for demonstration purposes
    print("AccountSid:", account_sid)
    print("CallSid:", call_sid)
    print("RecordingSid:", recording_sid)
    print("RecordingUrl:", recording_url)
    print("RecordingStatus:", recording_status)
    print("RecordingDuration:", recording_duration)
    print("RecordingChannels:", recording_channels)
    print("RecordingStartTime:", recording_start_time)
    print("RecordingSource:", recording_source)

    # Return a response to acknowledge the callback
    return 'Recording callback received'
    
if __name__ == "__main__":
    test.run(host='0.0.0.0', port=3000, debug=True)
