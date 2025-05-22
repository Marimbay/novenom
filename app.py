import os
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import json

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Load the model and processor
MODEL_NAME = "microsoft/resnet-50"  # We'll use ResNet-50 as a base model
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_image(image_path):
    try:
        # Load and preprocess the image
        image = Image.open(image_path)
        inputs = processor(images=image, return_tensors="pt")
        
        # Get model predictions
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            
        # Get the top prediction
        top_prob, top_class = torch.max(probabilities, dim=1)
        
        # For demonstration, we'll consider certain classes as potentially venomous
        # This is a simplified example - in a real application, you'd want to use a
        # model specifically trained for venomous creature detection
        venomous_classes = ['spider', 'snake', 'scorpion', 'wasp', 'bee']
        class_name = model.config.id2label[top_class.item()]
        
        # Check if the predicted class is in our venomous list
        is_venomous = any(venomous in class_name.lower() for venomous in venomous_classes)
        
        return {
            'is_venomous': is_venomous,
            'confidence': float(top_prob.item()),
            'class_name': class_name
        }
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
