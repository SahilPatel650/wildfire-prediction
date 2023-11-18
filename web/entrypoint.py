from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['GET'])
def run_script():
    # Code to execute your Python script
    import subprocess
    subprocess.run(["python3", "exec.py"])  # Replace 'your_script.py' with your actual script name
    return "Python script executed successfully!"

if __name__ == '__main__':
    app.run(debug=True)