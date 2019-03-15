FROM node:11-stretch-slim

COPY . /usr/local/src
WORKDIR /usr/local/src

RUN yarn install

ENTRYPOINT [ "yarn" ]
