import os

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

app.config["SECRET_KEY"] = "kalanod"


@app.route("/")
def hello():
    return "Hello, Flask!"


@app.route("/survey/<uuid>")
def survey(uuid):
    return render_template("survey.html")


@app.route("/api/survey/<uuid>", methods=["GET"])
def api_survey(uuid):
    try:
        # response = requests.get(f"http://app_manager:87/survey/get_survey_by_id/{uuid}")
        response = requests.get(f"http://localhost:80/get_survey_by_id/{uuid}")
        data = response.json()
        return jsonify({"status": "ok", "frontend_response": data})
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/api/survey/create_survey", methods=["POST"])
def create_survey():
    data = request.get_json()
    print("Received survey submission:")
    print(data)
    return jsonify({"status": "ok", "message": "Survey received"})


@app.route("/get_survey_by_id/<uuid>", methods=["GET"])
def get_survey_by_id(uuid):
    survey = {
        "title": "Customer Feedback Survey",
        "id": "survey001",
        "questions": [
            {
                "id": "q16",
                "text": "What is your name? (ИНН или название компании)",
                "type": "tin",
                "required": True,
                "ansvers": [],
            },
            {
                "id": "q25",
                "text": "What is your favorite programming language?",
                "type": "str",
                "required": False,
                "ansvers": [],
            },
            {
                "id": "q24",
                "text": "What is your favorite programming language?",
                "type": "str",
                "required": False,
                "ansvers": [],
            },
            {
                "id": "q23",
                "text": "What is your favorite programming language?",
                "type": "str",
                "required": False,
                "ansvers": [],
            },
            {
                "id": "q22",
                "text": "What is your favorite programming language?",
                "type": "str",
                "required": False,
                "ansvers": [],
            },
            {
                "id": "q21",
                "text": "What is your favorite programming language?",
                "type": "str",
                "required": False,
                "ansvers": [],
            },
            {
                "id": "q3",
                "text": "How would you rate our service?",
                "type": "int",
                "required": True,
                "ansvers": [],
                "min": 0,
                "max": 10,
            },
            {"id": "q4", "text": "Do you like our product?", "type": "bool", "required": True, "ansvers": ["yes", "no"]},
            {"id": "q5", "text": "When does the survey end?", "type": "datetime", "required": False, "ansvers": []},
        ],
    }
    return jsonify(survey)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
