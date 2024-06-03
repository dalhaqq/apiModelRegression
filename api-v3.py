#app.py
import os
from werkzeug.utils import secure_filename
from pricecounter import getprice, getpage
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.api_key = "fD9BkZUwQpVgxw7zLsC3YK9eF6u5J2mN"
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/api/v3/upload', methods=['POST'])
def upload_file():
    api_key = request.headers.get('api-key')
    if api_key is None or api_key != app.api_key:
        return jsonify({'error': 'Unauthorized'}), 401

    if request.content_length > 50 * 1024 * 1024:  # 50 MB
        return jsonify({'error': 'Max file size 50 MB exceeded'}), 400

    file = request.files.get('file')
    if file is None:
        return jsonify({'message': 'No file part in the request'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        price = getprice(file_path)
        page = getpage(file_path)
        return jsonify({'message': 'File processed', 'price': price, 'page':page, 'bw_price': 300*page}), 200
    finally:
        os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)
