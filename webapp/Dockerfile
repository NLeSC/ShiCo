FROM node:alpine

COPY . /home/shico
WORKDIR /home/shico

RUN npm install -g gulp
RUN npm install .

CMD /home/shico/dockerRun.sh
