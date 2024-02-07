FROM node:19 AS node-build

WORKDIR /usr/src/app

COPY Accuracy-Test/package*.json ./
RUN npm install

COPY Accuracy-Test/ .

RUN npm run build

ENTRYPOINT [ "/bin/sh", "-c" , "node build" ]
