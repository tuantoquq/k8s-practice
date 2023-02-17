FROM node:alpine as build

WORKDIR /front-end

COPY package.json .

RUN npm install

COPY . . 

RUN npm run build

#Nginx config

FROM nginx 

COPY --from=build /front-end/build /usr/share/nginx/html

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]