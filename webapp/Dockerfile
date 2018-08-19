FROM node:alpine

COPY . /home/shico
WORKDIR /home/shico

RUN apk update && apk add git

RUN npm install -g gulp bower
RUN npm install .
RUN bower install --config.interactive=false --allow-root

CMD /home/shico/dockerRun.sh
