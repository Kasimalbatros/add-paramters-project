from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    environment = os.getenv('ENVIRONMENT', 'development')
    return render_template('index.html', environment=environment)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
