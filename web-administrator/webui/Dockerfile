FROM node:alpine as build

WORKDIR /webui

COPY package.json .

RUN npm install

COPY . . 

RUN npm run build

#Nginx config

FROM nginx 

COPY --from=build /webui/build /usr/share/nginx/html

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]