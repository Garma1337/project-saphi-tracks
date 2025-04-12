FROM node:23.9 AS build

WORKDIR /app

COPY web/package*.json ./
RUN npm install

COPY web .
RUN npm run build

FROM nginx:alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
