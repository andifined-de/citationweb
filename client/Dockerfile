FROM node:18

WORKDIR /src

RUN npm i -g @angular/cli

ADD package.json /src
RUN npm i --silent
ADD . /src
RUN npm run build
CMD npm start

# COPY . .
