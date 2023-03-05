FROM node:alpine as build

WORKDIR /app

COPY package.json .

RUN npm install

COPY . . 

RUN npm run build

#Nginx config

FROM nginx 

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]