from flask import Flask, render_template, request, send_file
import os
import json
from utils.processor import process_sheet

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload_folder'
app.config['PROCESSED_FOLDER'] = 'processed_sheets'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Load publisher formats from JSON
with open('publisher_config.json') as f:
    PUBLISHER_FORMATS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', publishers=PUBLISHER_FORMATS.keys())

@app.route('/upload', methods=['POST'])
def upload_file():
    publisher = request.form.get('publisher')
    file = request.files.get('file')

    if not file or publisher not in PUBLISHER_FORMATS:
        return "Invalid publisher or file", 400

    # Save uploaded file
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(upload_path)

    # Process the file
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], f"processed_{file.filename}")
    process_sheet(upload_path, processed_path, PUBLISHER_FORMATS[publisher])

    return send_file(processed_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
