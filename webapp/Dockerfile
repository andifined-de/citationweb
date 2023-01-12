FROM node:18-alpine AS build



# install dependencies
WORKDIR /
COPY package.json package-lock.json ./
RUN npm install
RUN npm ci

# Copy all local files into the image.
COPY . .

RUN npm run build

###
# Only copy over the Node pieces we need
# ~> Saves 35MB
###
FROM node:18-alpine AS run

WORKDIR /
COPY --from=build / .
COPY . .


EXPOSE 3000
CMD ["node", "./app.js"]
