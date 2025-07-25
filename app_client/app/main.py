import logging

import requests

# from asgiref.wsgi import WsgiToAsgi
from config.settings import settings
from flask import (Flask, Response, jsonify, redirect, render_template,
                   request, session, url_for)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],  # Вывод в консоль  # Запись в файл
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.SECRET_KEY
# asgi_app = WsgiToAsgi(app)


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
    return '''
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;background:linear-gradient(135deg,#f5f7fa 0%,#c3cfe2 100%);font-family:sans-serif;">
        <img src="/static/tmk_logo.png" alt="Логотип" style="height:80px;margin-bottom:24px;">
        <h1 style="color:#2d3a4a;font-size:2.5em;margin-bottom:8px;">Добро пожаловать в сервис опросов!</h1>
        <div style="color:#4a6073;font-size:1.3em;margin-bottom:32px;max-width:500px;text-align:center;">
            Здесь вы можете пройти опросы, оставить обратную связь и помочь нам стать лучше.<br>Спасибо, что выбираете нас!
        </div>
        <a href="/survey/demo" style="background:#f47832;color:#fff;padding:14px 36px;border-radius:8px;font-size:1.2em;text-decoration:none;box-shadow:0 2px 8px rgba(0,0,0,0.08);transition:background 0.2s;">Пройти демо-опрос</a>
    </div>
    '''


@app.route('/survey1/demo')
def survey1():
    return render_template('survey.html')


@app.route("/survey/<uuid>")
def survey(uuid):
    return render_template("survey.html")


@app.route("/api/survey/<uuid>", methods=["GET"])
def api_survey(uuid):
    try:
        # response = requests.get(f"http://app_manager:8002/survey/get_survey_by_id/{uuid}")
       
        response = requests.get(f"http://localhost:{settings.CLIENT_PORT}/get_survey_by_id/{uuid}")
        data = response.json()
        return jsonify({"status": "ok", "frontend_response": data})
    except Exception as e:
        logger.error(str(e))
        return jsonify({"status": "error", "message": str(e)})


@app.route("/api/survey/create_survey", methods=["POST"])
def create_survey():
    data = request.get_json()

    print('Received survey submission:')
    print(data)
    return jsonify({"status": "ok", "message": f"ваш промокод: {''.join(random.choices(string.ascii_letters + string.digits, k=10))}"})


@app.route("/get_survey_by_id/<uuid>", methods=["GET"])
def get_survey_by_id(uuid):
    survey = {
        "title": "Оценка качества продукции для покупателей металлических труб",
        "uuid": "survey001",
        "description": "Пожалуйста, оцените различные аспекты качества нашей продукции и обслуживания. Ваше мнение важно для нас!",
        "questions": [
            {"uuid": "q1", "text": "Оцените качество поверхности труб", "type": "rating", "required": True,
             "answers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "category": "1"},
            {"uuid": "q2", "text": "Оцените точность размеров труб", "type": "rating", "required": True,
             "answers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "category": "1"},
            {"uuid": "q3", "text": "Оцените прочность труб", "type": "rating", "required": True,
             "answers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "category": "1"},
            {"uuid": "q4", "text": "Оцените упаковку продукции", "type": "rating", "required": True,
             "answers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "category": "1"},
            {"uuid": "q5", "text": "Оцените соответствие продукции заявленным характеристикам", "type": "rating",
             "required": True, "answers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "category": "1"},
            {"uuid": "q6", "text": "Оцените скорость выполнения заказа", "type": "rating", "required": True,
             "answers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "category": "2"},
            {"uuid": "q7", "text": "Оцените работу менеджера", "type": "rating", "required": True,
             "answers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "category": "2"},
            {"uuid": "q8", "text": "Оцените удобство получения продукции (доставка/самовывоз)", "type": "rating",
             "required": True, "answers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "category": "2"},
            {"uuid": "q9", "text": "Какие дополнительные услуги вы бы хотели видеть? (можно выбрать несколько)",
             "type": "checkbox", "required": False,
             "answers": ["Резка труб", "Покраска", "Доставка до объекта", "Складирование", "Сертификация"],
             "category": None},
            {"uuid": "q10", "text": "Какой способ связи для вас предпочтительнее?", "type": "radio", "required": False,
             "answers": ["Телефон", "Email", "Мессенджеры", "Личный кабинет"], "category": None},
            {"uuid": "q11", "text": "Порекомендуете ли вы нашу продукцию другим?", "type": "bool", "required": True,
             "answers": ["Да", "Нет"], "category": None},
            {"uuid": "q12", "text": "Ваши пожелания и комментарии (открытый вопрос)", "type": "text", "required": False,
             "answers": [], "category": None},
            {"uuid": "q13", "text": "Спасибо за участие в опросе! Ваши ответы помогут нам стать лучше.", "type": "text",
             "required": False, "answers": [], "category": None}
        ]
    }
    return jsonify(survey)
    try:
        response = requests.get(f"http://app_manager:8002/calculator/dashboard/{uuid}")
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/admin")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    return render_template("admin.html")


@app.route("/admin/get_all_surveys")
def get_all_surveys():
    return jsonify([
        {
            "uuid": "demo",
            "name": "demo",
            "start_date": "2025-07-22T09:59:27.442000+03:00",
            "end_date": "2025-07-22T09:59:27.442000+03:00",
            "manager_id": "2754f397-012f-4919-8faa-95cb1d45b656"
        }
    ])
    try:
        response = requests.get(f"http://app_manager:8002/admin/get_all_surveys/")
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})



@app.route("/admin/get_stat/<uuid>")
def get_stat(uuid):

      
    try:
        response = requests.get(f"http://{settings.MANAGER_HOST}:{settings.MANAGER_PORT}/calculator/dashboard/{uuid}")
        data = response.text
        return Response(data, content_type="application/json; charset=utf-8")  # фиксит енкодинг
        # data = response.json()
        # return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=settings.CLIENT_PORT, threaded=True)
