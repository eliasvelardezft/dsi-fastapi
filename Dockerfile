# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . .

# Expose the port on which the FastAPI server will run (change it to the appropriate port)
EXPOSE 8000

# Start the FastAPI server when the container starts
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]