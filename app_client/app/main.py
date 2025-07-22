import os

import requests
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from config.settings import settings

app = Flask(__name__)

app.config["SECRET_KEY"] = "kalanod"


# --- AUTH ---
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_panel"))
        else:
            error = "Неверный логин или пароль"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("login"))


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
        # response = requests.get(f"http://{settings.MANAGER_HOST}:{settings.MANAGER_PORT}/get_survey_by_id/{uuid}")
        response = requests.get(f"http://localhost:{settings.CLIENT_PORT}/get_survey_by_id/{uuid}")
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
        "title": "title",
        "uuid": "survey001",
        "questions": [
            {
                "uuid": "q1",
                "text": "ИНН или название компании",
                "type": "tin",
                "required": True,
                "answers": [],
                "category": "1",
            },
            {"uuid": "q2", "text": "text", "type": "text", "required": False, "answers": [], "category": "1"},
            {
                "uuid": "q3",
                "text": "How would you rate our service?",
                "type": "rating",
                "required": True,
                "answers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "category": "1",
            },
            {
                "uuid": "q4",
                "text": "Do you like our product?",
                "type": "bool",
                "required": True,
                "answers": ["yes", "no"],
                "category": "1",
            },
            {
                "uuid": "q5",
                "text": "When does the survey end?",
                "type": "datetime",
                "required": False,
                "answers": [],
                "category": "1",
            },
            {
                "uuid": "q6",
                "text": "what do you like",
                "type": "radio",
                "required": False,
                "answers": ["fruits", "kalans", "home"],
                "category": None,
            },
            {
                "uuid": "q7",
                "text": "what do you like",
                "type": "checkbox",
                "required": False,
                "answers": ["fruits", "kalans", "home"],
                "category": None,
            },
        ],
    }
    return jsonify(survey)


@app.route("/admin")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    return render_template("admin.html")


@app.route("/admin/get_all_surveys")
def get_all_surveys():
    # Заглушка: возвращаем тестовые данные
    return jsonify({"survey001": "Опрос по продукту", "survey002": "Оценка сервиса", "survey003": "Фидбек клиентов"})


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
