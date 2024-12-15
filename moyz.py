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

# File extensions allowed for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML for homepage
homepage_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pixel Compress</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px;">
    <h1 style="color: #333;">Welcome to Pixel Compress</h1>
    <p style="color: #555;">Compress your images in a pixelated style</p>
    <a href="/compress" style="padding: 10px 20px; background: #007BFF; color: white; text-decoration: none; border-radius: 5px;">Start Compressing</a>
</body>
</html>
'''

# HTML for compression page
compress_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Compress Image</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px;">
    <h1 style="color: #333;">Compress Your Image</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required style="margin: 20px 0; padding: 10px;">
        <input type="number" name="quality" min="1" max="100" placeholder="Quality (1-100)" required style="margin: 10px 0; padding: 10px;">
        <button type="submit" style="padding: 10px 20px; background: #007BFF; color: white; border: none; border-radius: 5px;">Upload and Compress</button>
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
    if file.filename == '':
        return "No selected file", 400
    
    if not allowed_file(file.filename):
        return "Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.", 400
    
    # Save the file securely
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)
    print(f"File saved to: {file_path}")

    # Compress the image
    compressed_path = os.path.join(COMPRESSED_FOLDER, secure_filename(file.filename))
    print(f"Compressing file to: {compressed_path}")
    
    quality = int(request.form.get('quality', 50))  # Default quality is 50
    image = Image.open(file_path)
    image.save(compressed_path, optimize=True, quality=quality)
    print(f"File successfully compressed: {compressed_path}")

    # Send the compressed file back to the user
    return send_file(compressed_path, as_attachment=True)

@app.errorhandler(500)
def internal_error(error):
    return "An internal error occurred. Please try again later.", 500

if _name_ == '_main_':
    app.run(debug=False, host='0.0.0.0', port=5000)
    
