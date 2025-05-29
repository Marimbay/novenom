import os
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import requests
import base64

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# AI Server configuration
AI_SERVER_URL = "http://10.88.17.11:5001/analyze"  # Replace with your laptop's IP address

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_image(image_path):
    try:
        # Read image and convert to base64
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Send to AI server
        response = requests.post(AI_SERVER_URL, json={'image': image_data})
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error from AI server: {response.text}")
            return None
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    error = None
    image_url = None
    result = None
    confidence = None
    class_name = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file part'
        else:
            file = request.files['file']
            if file.filename == '':
                error = 'No selected file'
            elif allowed_file(file.filename):
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = url_for('static', filename=f'uploads/{filename}')

                # Analyze the image
                analysis = analyze_image(filepath)
                if analysis:
                    result = "Potentially Venomous ⚠️" if analysis['is_venomous'] else "Safe ✅"
                    confidence = f"{analysis['confidence']:.2%}"
                    class_name = analysis['class_name']
                else:
                    error = 'Error analyzing image'

            else:
                error = 'File type not allowed'

    return render_template('upload.html',
                         error=error,
                         image_url=image_url,
                         result=result,
                         confidence=confidence,
                         class_name=class_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
