FROM python:3.6
WORKDIR /APP
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_APP server.py
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN bash ./get_ip.sh
CMD ["flask", "run"]

