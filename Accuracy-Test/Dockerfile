FROM node:18.19.0 AS node-build

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

ENTRYPOINT [ "/bin/sh", "-c" , "node build" ]
