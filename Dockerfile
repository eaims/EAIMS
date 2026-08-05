FROM nginx:1.27-alpine
COPY site/ /usr/share/nginx/html/site/
COPY assessment/questionnaire.json /usr/share/nginx/html/assessment/questionnaire.json
RUN printf 'server { listen 80; root /usr/share/nginx/html; location = / { return 302 /site/; } location / { try_files $uri $uri/ =404; } }' > /etc/nginx/conf.d/default.conf
EXPOSE 80
