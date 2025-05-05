FROM node:22.15-alpine

WORKDIR /app

COPY . .

RUN npm install --no-cache

EXPOSE 3000

RUN chmod +x run.sh

CMD ["npm", "run","dev" ,"--" ,"--host", "0.0.0.0"]
