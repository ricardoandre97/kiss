FROM docker.io/library/nginx:1.27.4-alpine

RUN rm -rf /usr/share/nginx/html/*

COPY index.html styles.css counters.js /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

EXPOSE 80
