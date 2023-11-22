# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /server
WORKDIR /server

# Copy all other files from the local directory to /server in the container
COPY . /server

# Install the Python dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Specify the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
