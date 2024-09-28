# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8300 available to the world outside this container
EXPOSE 8300

# Define environment variable
ENV NAME World

# Run backend.py when the container launches
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8300"]