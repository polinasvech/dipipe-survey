import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

app.config['SECRET_KEY'] = "mykey"  # Replace with a secure key in production


@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/api/survey')
def api_survey():
    # Example survey data with new type names and a rating (int) question
    survey = {
        "questions": [
            {"text": "What is your name? (ИНН или название компании)", "type": "tin"},
            {"text": "What is your favorite programming language?", "type": "str"},
            {"text": "How would you rate our service?", "type": "int", "min": 0, "max": 10},
            {"text": "Do you like our product?", "type": "bool"},
            {"text": "When does the survey end?", "type": "datetime"}
        ]
    }
    return jsonify(survey)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
