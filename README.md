# Twilio In-Browser Phone Application

This repository contains a Flask web application that integrates Twilio for voice functionality. The application allows users to make and receive phone calls directly from their browser.

## Setup

### Prerequisites

- Python 3.10
- Docker
- GitHub account
- Heroku account

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/zlehman1/twilio-inbrowserphone.git
   cd twilio-inbrowserphone
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Twilio and other API credentials:

   ```env
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_API_KEY=your_twilio_api_key
   TWILIO_API_SECRET=your_twilio_api_secret
   TWILIO_APP_SID=your_twilio_app_sid
   TWILIO_NUMBER=your_twilio_number
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   DEEPGRAM_API_KEY=your_deepgram_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running the Application

1. Start the Flask application:

   ```bash
   flask run
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000` to access the application.

## Deployment

### Deploying to Heroku using GitHub Actions

This repository includes a GitHub Actions workflow for deploying the application to Heroku using Docker.

1. Set up the required GitHub secrets in your repository's settings:

   - `HEROKU_API_KEY`: Your Heroku API key
   - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
   - `TWILIO_API_KEY`: Your Twilio API Key
   - `TWILIO_API_SECRET`: Your Twilio API Secret
   - `TWILIO_APP_SID`: Your Twilio App SID
   - `TWILIO_NUMBER`: Your Twilio Number
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
   - `DEEPGRAM_API_KEY`: Your Deepgram API Key
   - `OPENAI_API_KEY`: Your OpenAI API Key

2. Push your changes to the `main` or `master` branch to trigger the deployment workflow.

The GitHub Actions workflow will build the Docker image, push it to the Heroku container registry, and release the application on Heroku.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
