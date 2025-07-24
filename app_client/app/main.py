import os

import requests
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import random
import string
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


@app.route('/survey/demo')
def survey():
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
    return jsonify({"status": "ok", "message": f"ваш промокод: {''.join(random.choices(string.ascii_letters + string.digits, k=10))}"})


@app.route('/get_survey_by_id/<uuid>', methods=['GET'])
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


@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/admin/get_all_surveys')
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


@app.route('/admin/get_stat<uuid>')
def get_stat(uuid):
    # Заглушка: возвращаем тестовые данные
    return jsonify({
  "uuid": "02fc2da7-c79b-40cd-b295-84fd2f960b93",
  "title": "Статистика по клиентам",
  "blocks": [
    {
      "diagrams": [
        {
          "uuid": "6dde9414-b794-4933-82a7-417f7da1c158",
          "title": "По дивизионам",
          "type": "bar",
          "categories": [
            {
              "label": "Урал",
              "value": 152,
              "color": "#e8a675"
            },
            {
              "label": "ДРТ",
              "value": 104,
              "color": "#ec6608"
            },
            {
              "label": "Волга",
              "value": 114,
              "color": "#887b73"
            },
            {
              "label": "Запад",
              "value": 98,
              "color": "#ffc000"
            },
            {
              "label": "ДРТ Юг",
              "value": 18,
              "color": "#adadad"
            },
            {
              "label": "Сибирь",
              "value": 190,
              "color": "#e8a675"
            }
          ]
        },
        {
          "uuid": "e7aeafc4-b2a8-4115-b2b9-34dcbc3d9768",
          "title": "По типам",
          "type": "round",
          "categories": [
            {
              "label": "Посредник (ДРТ)",
              "value": 14.2,
              "color": "#e8a675"
            },
            {
              "label": "Конечный потребитель",
              "value": 60.65,
              "color": "#ec6608"
            },
            {
              "label": "Посредник (дивизион)",
              "value": 16.27,
              "color": "#887b73"
            },
            {
              "label": "Металлотрейдер",
              "value": 8.88,
              "color": "#ffc000"
            }
          ]
        },
        {
          "uuid": "21f1fe77-ce2d-485b-bf51-e960b123db00",
          "title": "По преференциям",
          "type": "round",
          "categories": [
            {
              "label": "ВИП",
              "value": 10.36,
              "color": "#e8a675"
            },
            {
              "label": "Базовый",
              "value": 10.06,
              "color": "#ec6608"
            },
            {
              "label": "Розничный",
              "value": 50.3,
              "color": "#887b73"
            },
            {
              "label": "Оптовый",
              "value": 10.95,
              "color": "#ffc000"
            },
            {
              "label": "Мелкая розница",
              "value": 18.34,
              "color": "#adadad"
            }
          ]
        }
      ]
    },
    {
      "diagrams": [
        {
          "uuid": "ce273a06-24f5-4f9c-a82f-20cac9bb7b73",
          "title": "Лояльность",
          "type": "round",
          "categories": [
            {
              "label": "Критики",
              "value": 10.65,
              "color": "#fbfbfa"
            },
            {
              "label": "Нейтралы",
              "value": 14.79,
              "color": "#828583"
            },
            {
              "label": "Сторонники",
              "value": 74.56,
              "color": "#e7d49b"
            }
          ]
        },
        {
          "uuid": "2ed25e57-234b-450a-8508-2de43ba0c8cd",
          "title": "Удовлетворенность",
          "type": "round",
          "categories": [
            {
              "label": "Критики",
              "value": 13.61,
              "color": "#fbfbfa"
            },
            {
              "label": "Нейтралы",
              "value": 15.38,
              "color": "#828583"
            },
            {
              "label": "Сторонники",
              "value": 71.01,
              "color": "#e7d49b"
            }
          ]
        },
        {
          "uuid": "b70273ae-20b1-45f3-9a05-3c0d146d37f9",
          "title": "Вероятность повторной покупки",
          "type": "round",
          "categories": [
            {
              "label": "Критики",
              "value": 12.13,
              "color": "#fbfbfa"
            },
            {
              "label": "Нейтралы",
              "value": 18.34,
              "color": "#828583"
            },
            {
              "label": "Сторонники",
              "value": 69.53,
              "color": "#e7d49b"
            }
          ]
        }
      ]
    },
    {
      "diagrams": [
        {
          "uuid": "f6a84384-724b-4227-995e-74ee02bf2575",
          "title": "Удовлетворенность в разбивке по процессам",
          "type": "column",
          "categories": [
            {
              "label": "Удовлетворенность сроками предоставления коммерческого предложения",
              "value": 8.66272189349112,
              "color": "#e8a675"
            },
            {
              "label": "Оперативность выставления счета из наличия со складов ТД ТМК",
              "value": 8.99009900990099,
              "color": "#ec6608"
            },
            {
              "label": "Оперативность выставления счета из наличия заводов ТМК",
              "value": 8.71875,
              "color": "#887b73"
            },
            {
              "label": "Процесс согласования спецификации",
              "value": 8.79569892473118,
              "color": "#ffc000"
            },
            {
              "label": "Соблюдение сроков производства продукции",
              "value": 8.45414847161572,
              "color": "#adadad"
            },
            {
              "label": "Качество бесшовных труб",
              "value": 9.5705329153605,
              "color": "#e8a675"
            },
            {
              "label": "Качество сварных труб малого диаметра",
              "value": 9.41721854304636,
              "color": "#ec6608"
            },
            {
              "label": "Процесс претензионной работы",
              "value": 7.75728155339806,
              "color": "#887b73"
            },
            {
              "label": "Доступность информации в период работы исполнения заказа: готовность к отгрузке, изменение сроков поставки и т.д.",
              "value": 9.00887573964497,
              "color": "#ffc000"
            },
            {
              "label": "Работа вашего менеджера",
              "value": 9.16863905325444,
              "color": "#adadad"
            },
            {
              "label": "Организация процесса самовывоза с заводов или складов ТМК",
              "value": 8.20863309352518,
              "color": "#e8a675"
            },
            {
              "label": "Услуга доставки продукции",
              "value": 8.87804878048781,
              "color": "#ec6608"
            },
            {
              "label": "Качество консультаций операторов ЕКЦ",
              "value": 8.86904761904762,
              "color": "#887b73"
            }
          ]
        }
      ]
    },
    {
      "diagrams": [
        {
          "uuid": "e24ae211-0a48-4177-be4b-5c55cf52047e",
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
        }
      ]
    }
  ]
})
    try:
        response = requests.get(f"http://app_manager:8002/admin/get_stat/{uuid}")
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/admin/proxy_get_all_surveys')
def proxy_get_all_surveys():
    # Заглушка: возвращаем тестовые данные в новом формате
    return jsonify([
        {
            "uuid": "b8be6e48-eee2-49bb-b7b4-5654947d3fac",
            "name": "string",
            "start_date": "2025-07-22T07:16:23.694000+03:00",
            "end_date": "2025-07-22T07:16:23.694000+03:00",
            "manager_id": "2754f397-012f-4919-8faa-95cb1d45b656"
        },
        {
            "uuid": "demo",
            "name": "demo",
            "start_date": "2025-07-22T09:59:27.442000+03:00",
            "end_date": "2025-07-22T09:59:27.442000+03:00",
            "manager_id": "2754f397-012f-4919-8faa-95cb1d45b656"
        }
    ])
    try:
        response = requests.get(f"http://app_manager:8002/admin/get_all_surveys")
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/admin/proxy_get_stat/<uuid>')
def proxy_get_stat(uuid):
    # Заглушка: возвращаем тестовые данные для статистики опроса
    return jsonify({
        "id": "07215c16-a036-4924-967d-2d50f788e81b",
        "survey_id": uuid,
        "count": 1,
        "answers": [
            {
                "uuid": "5519651a-6df2-4a91-acc5-030ad587dedd",
                "client_id": "1c5a8d0b-f296-4d33-acde-684edf7cc32f",
                "survey_id": uuid,
                "question_id": "0b5f20b5-3119-4829-b5fc-6d75eab915cd",
                "answer_int": 0,
                "answer_text": "string",
                "question": None
            }
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
