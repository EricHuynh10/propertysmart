# Use an official Node runtime as the base image
FROM node:14

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Bundle app source
COPY . .

# Build the app
RUN npm run build

# Use an official lightweight Node.js runtime for the final image
FROM nginx:alpine

# Copy build files from builder stage to nginx html directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port 80 for the app
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
