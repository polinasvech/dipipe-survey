FROM python:3.12.3
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/app

# COPY requirements.txt requirements.txt
#
# RUN  pip install  --trusted-host pypi.org --trusted-host files.pythonhosted.org --disable-pip-version-check --no-cache-dir --upgrade pip \
#      && pip install  --trusted-host pypi.org --trusted-host files.pythonhosted.org --disable-pip-version-check --no-cache-dir -r  requirements.txt
#
# COPY run_app.sh run_app.sh
# #делаем файл исполняемым
# RUN chmod +x run_app.sh

COPY . .

# ENTRYPOINT ["bash", "run_app.sh"]