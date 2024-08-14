# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to avoid buffering issues
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . /app

# Expose any ports if your application requires it (optional)
# EXPOSE 5000

# Set the command to run the application
CMD ["python", "main.py"]
