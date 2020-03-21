FROM strapi/base

ENV NODE_ENV production
EXPOSE 1337

COPY package.json package.json
COPY yarn.lock yarn.lock

RUN yarn --frozen-lockfile

COPY . .

RUN yarn build

CMD ["yarn", "start"]
