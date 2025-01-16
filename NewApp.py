# Google search create docker image for flask app using dynamic render_template
# Use a Python base image
# FROM python:3.9-slim-buster
FROM python:3.10.15-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0"]

docker build -t my-flask-app .

docker run -d -p 5000:5000 my-flask-app 

# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {'name': 'John', 'age': 30}
    return render_template('index.html', **data)

if __name__ == '__main__':
    app.run(debug=True)

# templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Flask App</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
    <p>You are {{ age }} years old.</p>
</body>
</html>