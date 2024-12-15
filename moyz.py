import streamlit as st
from PIL import Image
import os

app = Flask(__name__)

# Set upload and compressed folder paths to the user's home directory
UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'uploads')
COMPRESSED_FOLDER = os.path.join(os.path.expanduser('~'), 'compressed')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

# Homepage HTML
homepage_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pixel Compress</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #1e1e2f;
            color: #fff;
            margin: 0;
            text-align: center;
            padding: 50px;
            image-rendering: pixelated;
        }
        .container {
            display: inline-block;
            background: #3a3a5a;
            border: 4px solid #0056b3;
            box-shadow: 4px 4px #003366;
            padding: 30px;
            border-radius: 8px;
            width: 300px;
        }
        h1 {
            color: #66a3ff;
            font-size: 32px;
            text-transform: uppercase;
        }
        p {
            color: #cce6ff;
        }
        .btn {
            font-size: 20px;
            background-color: #0056b3;
            color: #ffffff;
            padding: 10px 20px;
            border: 2px solid #003366;
            border-radius: 4px;
            text-decoration: none;
            cursor: pointer;
            box-shadow: 2px 2px #003366;
            display: block;
            margin: 10px auto;
        }
        .btn:hover {
            background-color: #66a3ff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Pixel Compress</h1>
        <p>Compress your photos in a pixelated style!</p>
        <a href="/compress" class="btn">Start Compressing</a>
        <a href="/report" class="btn">View Report</a>
    </div>
</body>
</html>
'''

# Compress Page HTML
compress_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compress Image</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.12/cropper.min.css" />
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #1e1e2f;
            color: #fff;
            margin: 0;
            text-align: center;
            padding: 50px;
            image-rendering: pixelated;
        }
        .container {
            display: inline-block;
            background: #3a3a5a;
            border: 4px solid #0056b3;
            box-shadow: 4px 4px #003366;
            padding: 30px;
            border-radius: 8px;
            width: 300px;
        }
        h1 {
            color: #66a3ff;
            font-size: 32px;
            text-transform: uppercase;
        }
        input[type="file"] {
            display: block;
            margin: 20px auto;
            padding: 5px;
            border: 2px dashed #66a3ff;
            background-color: #3a3a5a;
            color: #cce6ff;
            width: 80%;
            text-align: center;
        }
        .btn {
            font-size: 20px;
            background-color: #0056b3;
            color: #ffffff;
            padding: 10px 20px;
            border: 2px solid #003366;
            border-radius: 4px;
            cursor: pointer;
            box-shadow: 2px 2px #003366;
        }
        .btn:hover {
            background-color: #66a3ff;
 ```python
        }
    </style>
 </head>
<body>
    <div class="container">
        <h1>Compress Your Image</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button type="submit" class="btn">Upload and Compress</button>
        </form>
        <div id="cropper-container"></div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.12/cropper.min.js"></script>
    <script>
        const input = document.querySelector('input[type="file"]');
        let cropper;

        input.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const image = document.createElement('img');
                    image.src = e.target.result;
                    document.body.appendChild(image);
                    cropper = new Cropper(image, {
                        aspectRatio: 16 / 9,
                        viewMode: 1,
                        autoCropArea: 1,
                        ready() {
                            // Crop the image when ready
                        },
                    });
                };
                reader.readAsDataURL(file);
            }
        });

        document.querySelector('form').addEventListener('submit', (event) => {
            event.preventDefault();
            const canvas = cropper.getCroppedCanvas();
            canvas.toBlob((blob) => {
                const formData = new FormData();
                formData.append('image', blob, 'cropped.jpg');

                fetch('/upload', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'compressed.jpg';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                })
                .catch(() => alert('Error uploading image'));
            });
        });
    </script>
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
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Compress the image
        compressed_path = os.path.join(COMPRESSED_FOLDER, file.filename)
        image = Image.open(file_path)
        image.save(compressed_path, optimize=True, quality=50)  # Adjust quality as needed
        
        return send_file(compressed_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    
