FROM node:16.4-alpine3.14 as base

LABEL version="1.0"

RUN apk update && apk add --no-cache nmap && \
    echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories && \
    echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache \
      chromium \
      harfbuzz \
      "freetype>2.8" \
      ttf-freefont \
      nss
WORKDIR /app

COPY ["package.json", "yarn.lock", "./"]

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
RUN yarn install

EXPOSE 3000

from base as test

COPY . .
RUN yarn test --watchAll=false

from test as local

CMD ["yarn", "run", "start"]

from base as builder

COPY ./ /app

RUN yarn run build

from nginx:1.20.1-alpine as optimized

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/build /usr/share/nginx/html

RUN addgroup -S scaffold && adduser -S scaffold -G scaffold

USER scaffold

# copied from ngingx Dockerfile
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
