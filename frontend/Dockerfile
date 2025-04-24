FROM node:alpine

WORKDIR /app

COPY . .

RUN npm install --no-cache

EXPOSE 3000

RUN chmod +x run.sh

CMD ["./run.sh"]
