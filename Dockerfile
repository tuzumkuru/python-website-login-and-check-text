FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY main.py requirements.txt .env ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install ChromeDriver
RUN apt-get update && apt-get install -y chromium-driver

# Run the Selenium script when the container launches
CMD ["python", "-u", "main.py"]
