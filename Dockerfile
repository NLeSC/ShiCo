FROM python:2.7.12

COPY . /home/shico
WORKDIR /home/shico
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD /home/shico/dockerRun.sh
