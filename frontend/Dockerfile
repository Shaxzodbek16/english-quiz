FROM node:alpine

WORKDIR /app

COPY . .

RUN npm install --no-cache

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
