FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN echo "Asia/Shanghai" > /etc/timezone

COPY requirements.txt /app/

RUN pip install nb-cli
RUN pip install -r requirements.txt

RUN nb plugin install nonebot_plugin_apscheduler
RUN nb plugin install nonebot_plugin_status