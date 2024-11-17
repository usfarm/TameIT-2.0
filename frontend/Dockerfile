FROM node:14-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Set environment variables
ENV NODE_ENV=development
ENV PATH /app/node_modules/.bin:$PATH

EXPOSE 3000

CMD ["npm", "start"]