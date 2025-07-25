FROM python:3.12-slim

WORKDIR /opt/app

COPY app/requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app/ .

RUN chmod +x run.sh parse_excel.sh

CMD ["bash", "run.sh"]

