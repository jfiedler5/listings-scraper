# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /spider

# Copy the current directory contents into the container at /spider
COPY . /spider

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run scrapy when the container launches
CMD ["scrapy", "crawl", "sreality"]
