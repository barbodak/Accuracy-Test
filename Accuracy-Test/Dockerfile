FROM node:19 AS node-build

WORKDIR /usr/src/app

COPY Accuracy-Test/package*.json ./
RUN bun install

COPY Accuracy-Test/ .

RUN bun run build

ENTRYPOINT [ "/bin/sh", "-c" , "node build" ]
