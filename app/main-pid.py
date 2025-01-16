import docker
import os
import json

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello! from " + getProcessDetails() + " in a uWSGI Nginx Docker container with \
     Python 3.x (from the example template)"

@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, "index.html")

    # return send_file(index_path)
    templateData = {
            'title' : 'Container Demo!',
            'pid': getProcessDetails(),
            'cg-pid': get_container_id()    
         }

    return render_template('index.html', **templateData)

def getProcessDetails():
    try:
        client = docker.from_env()

        # Get the container object
        container = client.containers.get('demoapp')

        # Get the top process information
        top_info = container.top()

        # Extract the PID of the top process
        pid = top_info['Processes'][0][0]
    except:
        pid = os.getpid()

    return str(pid)

def get_container_id():
    try:
        with open("/proc/self/cgroup", "r") as f:
            for line in f:
                if "docker" in line:
                    return line.split("/")[-1].strip()
    except:
        return "Running locally"

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)

# lsof -i:80 
# kill -9 <pid>