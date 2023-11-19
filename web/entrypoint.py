from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
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
    filepath = random_string + '.png'
    print(filepath)

    data = request.json
    grid_data = data['gridData']
    grid_data_str = json.dumps(grid_data)


    import subprocess
    # Code to execute your Python script
    subprocess.run(["python3", "main.py", grid_data_str, filepath])
    return jsonify({'filepath': filepath})

@app.route('/get_dynamic_image')
def get_dynamic_image():
    # Your logic to determine the image
    image_filename = 'uploads/image.png'
    return url_for('static', filename=image_filename)


@app.route('/uploads/<path>')
def get_upload(path):
    # Your logic to determine the image
    fn = 'uploads/' + path
    print(fn)
    return url_for('static', filename=fn)



if __name__ == '__main__':
    app.run(debug=True)
