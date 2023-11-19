from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():

    data = request.json
    grid_data = data['gridData']
    grid_data_str = json.dumps(grid_data)
    # print(grid_data)

    import subprocess
    # Code to execute your Python script
    subprocess.run(["python3", "main.py", grid_data_str])  # Replace 'your_script.py' with your actual script name
    return jsonify({"message": "Python script executed successfully!"})

if __name__ == '__main__':
    app.run(debug=True)