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
    # Example survey data with new structure
    survey = {
        "title": "Customer Feedback Survey",
        "id": "survey001",
        "questions": [
            {
                "id": "q1",
                "text": "What is your name? (ИНН или название компании)",
                "type": "tin",
                "required": True,
                "ansvers": []
            },
            {
                "id": "q2",
                "text": "What is your favorite programming language?",
                "type": "str",
                "required": False,
                "ansvers": []
            },
            {
                "id": "q3",
                "text": "How would you rate our service?",
                "type": "int",
                "required": True,
                "ansvers": [],
                "min": 0,
                "max": 10
            },
            {
                "id": "q4",
                "text": "Do you like our product?",
                "type": "bool",
                "required": True,
                "ansvers": ["yes", "no"]
            },
            {
                "id": "q5",
                "text": "When does the survey end?",
                "type": "datetime",
                "required": False,
                "ansvers": []
            }
        ]
    }
    return jsonify(survey)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
