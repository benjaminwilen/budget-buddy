FROM node:18 AS build

WORKDIR /Users/benjaminwilen/budget-buddy/budget_buddy/frontend

COPY package.json .
RUN npm install

COPY . .
RUN npm run build

FROM node:18 AS production
WORKDIR /Users/benjaminwilen/budget-buddy/budget_buddy/frontend
COPY --from=build ./build ./build

RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]

EXPOSE 3000
