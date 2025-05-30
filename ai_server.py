from flask import Flask, request, jsonify
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import base64
import io

app = Flask(__name__)

# Load the model and processor
MODEL_NAME = "microsoft/resnet-50"
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

def analyze_image(image_data):
    try:
        # Convert base64 to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Process image
        inputs = processor(images=image, return_tensors="pt")
        
        # Get model predictions
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            
        # Get the top prediction
        top_prob, top_class = torch.max(probabilities, dim=1)
        
        # Check for venomous creatures
        venomous_classes = ['spider', 'snake', 'scorpion', 'wasp', 'bee']
        class_name = model.config.id2label[top_class.item()]
        is_venomous = any(venomous in class_name.lower() for venomous in venomous_classes)
        
        return {
            'is_venomous': is_venomous,
            'confidence': float(top_prob.item()),
            'class_name': class_name
        }
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return None

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.json:
        return jsonify({'error': 'No image data provided'}), 400
    
    image_data = request.json['image']
    result = analyze_image(image_data)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Error processing image'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 