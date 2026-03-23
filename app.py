from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/')
def home():
    version = os.environ.get('APP_VERSION', '1.0.0')
    return f'hello from backend v{version}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
