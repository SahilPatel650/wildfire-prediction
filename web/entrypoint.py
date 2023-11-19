from flask import Flask, render_template, request, jsonify, send_from_directory
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    #create a random 8 character string in python
    import random
    import string
    letters = string.ascii_uppercase
    random_string = ''.join(random.choice(letters) for i in range(8))
    #make it into a filepath for a jpg
    filepath = "web/uploads/" + random_string + ".png"
    print(filepath)


    data = request.json
    grid_data = data['gridData']
    grid_data_str = json.dumps(grid_data)
    # print(grid_data)

    import subprocess
    # Code to execute your Python script
    # subprocess.run(["python3", "main.py", grid_data_str, filepath])  # Replace 'your_script.py' with your actual script name
    return jsonify({'filepath': filepath})

if __name__ == '__main__':
    app.run(debug=True)
