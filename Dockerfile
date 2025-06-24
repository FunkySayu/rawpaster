# Stage 1: Build Angular frontend
FROM node:18 AS build-angular

WORKDIR /app/frontend

# Copy package.json and package-lock.json (if available)
COPY frontend/package.json frontend/package-lock.json* ./

# Install Angular CLI locally for the build (safer than relying on global)
RUN npm install @angular/cli@latest

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Build Angular app for production
RUN ng build --configuration production

# Stage 2: Python/Nginx runtime
FROM python:3.9-slim

WORKDIR /app

# Install Nginx and Gunicorn
RUN apt-get update && \
    apt-get install -y nginx gettext-base && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies for Flask app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app source code
COPY app.py .
COPY utils.py .
COPY config.py .
COPY data/ ./data/ # Assuming data needs to be in the image, or use a volume
COPY authorized_keys.txt . # Assuming this is the initial set of keys

# Copy built Angular app from Stage 1
COPY --from=build-angular /app/frontend/dist/frontend /app/static

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port (Nginx will listen on 80 by default)
EXPOSE 80

# Command to run the startup script
CMD ["/start.sh"]
