from flask import Flask, render_template_string, request, send_file
from PIL import Image
from werkzeug.utils import secure_filename
import os

app = Flask(_name_)

# Set upload and compressed folder paths
UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'uploads')
COMPRESSED_FOLDER = os.path.join(os.path.expanduser('~'), 'compressed')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

homepage_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pixel Compress</title>
</head>
<body>
    <h1>Welcome to Pixel Compress</h1>
    <a href="/compress">Start Compressing</a>
</body>
</html>
'''

compress_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Compress Image</title>
</head>
<body>
    <h1>Compress Your Image</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required>
        <input type="number" name="quality" min="1" max="100" placeholder="Quality (1-100)" required>
        <button type="submit">Upload and Compress</button>
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(homepage_html)

@app.route('/compress')
def compress():
    return render_template_string(compress_html)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No file part", 400
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return "Invalid file type", 400
    quality = int(request.form.get('quality', 50))  # Default 50 if not provided
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)

    compressed_path = os.path.join(COMPRESSED_FOLDER, secure_filename(file.filename))
    image = Image.open(file_path)
    image.save(compressed_path, optimize=True, quality=quality)

    return send_file(compressed_path, as_attachment=True)

if _name_ == '_main_':
    app.run(debug=False, host='0.0.0.0', port=5000)
