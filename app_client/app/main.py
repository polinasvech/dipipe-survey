import os

import requests
from flask import Flask, render_template, jsonify, request, redirect, url_for, session

app = Flask(__name__)

app.config['SECRET_KEY'] = "kalanod"


# --- AUTH ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = 'Неверный логин или пароль'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))


@app.route('/')
def hello():
    return 'Hello, Flask!'


@app.route('/survey/<uuid>')
def survey(uuid):
    return render_template('survey.html')


@app.route('/api/survey/<uuid>', methods=['GET'])
def api_survey(uuid):
    try:
        # response = requests.get(f"http://app_manager:8002/survey/get_survey_by_id/{uuid}")
        response = requests.get(f"http://localhost:80/get_survey_by_id/{uuid}")
        data = response.json()
        return jsonify({"status": "ok", "frontend_response": data})
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/api/survey/create_survey', methods=['POST'])
def create_survey():
    data = request.get_json()
    print('Received survey submission:')
    print(data)
    return jsonify({"status": "ok", "message": "Survey received"})


@app.route('/get_survey_by_id/<uuid>', methods=['GET'])
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
                "category": "1"
            },
            {
                "uuid": "q2",
                "text": "text",
                "type": "text",
                "required": False,
                "answers": [],
                "category": "1"
            },
            {
                "uuid": "q3",
                "text": "How would you rate our service?",
                "type": "rating",
                "required": True,
                "answers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "category": "1"
            },
            {
                "uuid": "q4",
                "text": "Do you like our product?",
                "type": "bool",
                "required": True,
                "answers": ["yes", "no"],
                "category": "1"
            },
            {
                "uuid": "q5",
                "text": "When does the survey end?",
                "type": "datetime",
                "required": False,
                "answers": [],
                "category": "1"
            },
            {
                "uuid": "q6",
                "text": "what do you like",
                "type": "radio",
                "required": False,
                "answers": ["fruits", "kalans", "home"],
                "category": None
            },
            {
                "uuid": "q7",
                "text": "what do you like",
                "type": "checkbox",
                "required": False,
                "answers": ["fruits", "kalans", "home"],
                "category": None
            }
        ]
    }
    return jsonify(survey)


@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/admin/get_all_surveys')
def get_all_surveys():
    return jsonify([
        {
            "uuid": "b8be6e48-eee2-49bb-b7b4-5654947d3fac",
            "name": "string",
            "start_date": "2025-07-22T07:16:23.694000+03:00",
            "end_date": "2025-07-22T07:16:23.694000+03:00",
            "manager_id": "2754f397-012f-4919-8faa-95cb1d45b656"
        },
        {
            "uuid": "aedaf34d-e899-4b4b-a76d-5fe2e8aac7c6",
            "name": "Второй",
            "start_date": "2025-07-22T09:59:27.442000+03:00",
            "end_date": "2025-07-22T09:59:27.442000+03:00",
            "manager_id": "2754f397-012f-4919-8faa-95cb1d45b656"
        }
    ])
    try:
        response = requests.get(f"http://app_manager:8002/admin/get_all_surveys/{uuid}")
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/admin/get_stat<uuid>')
def get_stat(uuid):
    # Заглушка: возвращаем тестовые данные
    return jsonify({
  "uuid": "ea2c5cc8-9495-472e-a27e-840a7229281e",
  "title": "Статистика по клиентам",
  "blocks": [
    {
      "diagrams": [
        {
          "uuid": "5194a9fa-b24d-4312-90f0-a7e15ec953a5",
          "title": "Удовлетворенность в разбивке по процессам",
          "type": "column",
          "categories": [
            {
              "label": "Удовлетворенность сроками предоставления коммерческого предложения",
              "value": 8.662721893491124,
              "color": "#AA0B5D"
            },
            {
              "label": "Оперативность выставления счета из наличия со складов ТД ТМК",
              "value": 8.990099009900991,
              "color": "#6384DD"
            },
            {
              "label": "Оперативность выставления счета из наличия заводов ТМК",
              "value": 8.71875,
              "color": "#1C45F1"
            },
            {
              "label": "Процесс согласования спецификации",
              "value": 8.795698924731182,
              "color": "#59A6E5"
            },
            {
              "label": "Соблюдение сроков производства продукции",
              "value": 8.45414847161572,
              "color": "#93444C"
            },
            {
              "label": "Качество бесшовных труб",
              "value": 9.570532915360502,
              "color": "#F36E10"
            },
            {
              "label": "Качество сварных труб малого диаметра",
              "value": 9.417218543046358,
              "color": "#186290"
            },
            {
              "label": "Процесс претензионной работы",
              "value": 7.757281553398058,
              "color": "#3A9A32"
            },
            {
              "label": "Доступность информации в период работы исполнения заказа: готовность к отгрузке, изменение сроков поставки и т.д.",
              "value": 9.00887573964497,
              "color": "#916A53"
            },
            {
              "label": "Работа вашего менеджера",
              "value": 9.168639053254438,
              "color": "#32F671"
            },
            {
              "label": "Организация процесса самовывоза с заводов или складов ТМК",
              "value": 8.20863309352518,
              "color": "#536B81"
            },
            {
              "label": "Услуга доставки продукции",
              "value": 8.878048780487806,
              "color": "#E583F5"
            },
            {
              "label": "Качество консультаций операторов ЕКЦ",
              "value": 8.869047619047619,
              "color": "#78218E"
            }
          ]
        }]},{
      "diagrams": [
        {
          "uuid": "0a76a198-7ea0-431c-bdb1-39830facd6ed",
          "title": "",
          "type": "table",
          "categories": [
            [
              ":)",
              "0.7",
              "0.76",
              "0.72",
              "0.74",
              "0.59",
              "0.89",
              "0.83",
              "0.57",
              "0.76",
              "0.82",
              "0.59",
              "0.75",
              "0.8"
            ],
            [
              ":|",
              "0.7",
              "0.76",
              "0.72",
              "0.74",
              "0.59",
              "0.89",
              "0.83",
              "0.57",
              "0.76",
              "0.82",
              "0.59",
              "0.75",
              "0.8"
            ],
            [
              ":(",
              "0.13",
              "0.09",
              "0.13",
              "0.11",
              "0.17",
              "0.03",
              "0.04",
              "0.25",
              "0.1",
              "0.09",
              "0.19",
              "0.13",
              "0.11"
            ]
          ]
        }]}
      ]
})
    try:
        response = requests.get(f"http://app_manager:8002/admin/get_stat/{uuid}")
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
