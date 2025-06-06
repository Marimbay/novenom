import os
from datetime import datetime
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
import requests
import base64
import sqlite3
from pathlib import Path
import atexit
import shutil
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

# Configure upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# Database configuration
DATABASE_PATH = os.path.join(app.root_path, 'novenom.db')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# AI Server configuration
AI_SERVER_URL = "http://10.89.56.215:5001/analyze"  # Replace with your laptop's IP address

def get_unique_filename(original_filename):
    """Generate a unique filename using UUID and original extension."""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    return f"{uuid.uuid4().hex}.{ext}"

def clean_species_name(name):
    """Clean and format the species name."""
    if not name:
        return "Unknown Species"
    
    # Split by comma and take the first part
    name = name.split(',')[0].strip()
    
    # Capitalize each word
    name = ' '.join(word.capitalize() for word in name.split())
    
    # Remove any extra spaces
    name = ' '.join(name.split())
    
    return name

def cleanup():
    """Clean up database and upload folder when the app exits."""
    try:
        # Delete all files in the upload folder
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
            os.makedirs(UPLOAD_FOLDER)
        
        # Clear the database
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM predictions')
        conn.commit()
        conn.close()
        
        app.logger.info("Cleanup completed successfully")
    except Exception as e:
        app.logger.error(f"Error during cleanup: {str(e)}")

# Register cleanup function to run on exit
atexit.register(cleanup)

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            is_venomous BOOLEAN NOT NULL,
            animal_name TEXT,
            confidence REAL,
            image_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_image(image_path):
    """Analyze an image using the AI server."""
    try:
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        response = requests.post(AI_SERVER_URL, json={'image': image_data})
        
        if response.status_code == 200:
            return response.json()
        else:
            app.logger.error(f"Error from AI server: {response.text}")
            return None
    except Exception as e:
        app.logger.error(f"Error analyzing image: {str(e)}")
        return None

def get_venom_status(is_venomous):
    """Get consistent venom status label."""
    return "Venomous" if is_venomous else "Not Venomous"

def save_prediction(filename, is_venomous, animal_name, confidence, image_url):
    """Save prediction results to the database."""
    try:
        conn = get_db()
        c = conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        
        # Clean up animal name
        animal_name = clean_species_name(animal_name)
        
        c.execute('''
            INSERT INTO predictions (filename, timestamp, is_venomous, animal_name, confidence, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filename, current_time, is_venomous, animal_name, confidence, image_url))
        conn.commit()
    except Exception as e:
        app.logger.error(f"Error saving prediction: {str(e)}")
    finally:
        conn.close()

@app.route('/', methods=['GET'])
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    """Handle image upload and analysis."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
            
        if not allowed_file(file.filename):
            flash('File type not allowed. Please upload an image (PNG, JPG, JPEG, or GIF)', 'error')
            return redirect(request.url)

        try:
            # Generate unique filename
            original_filename = secure_filename(file.filename)
            unique_filename = get_unique_filename(original_filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            image_url = url_for('static', filename=f'uploads/{unique_filename}')

            analysis = analyze_image(filepath)
            if analysis:
                is_venomous = analysis['is_venomous']
                result = get_venom_status(is_venomous)
                confidence = analysis['confidence']
                animal_name = clean_species_name(analysis['class_name'])
                
                # Save prediction to database
                save_prediction(unique_filename, is_venomous, animal_name, confidence, image_url)
                
                return render_template('upload.html',
                                     image_url=image_url,
                                     result=result,
                                     confidence=float(confidence * 100),
                                     confidence_text=f"{confidence:.2%}",
                                     animal_name=animal_name)
            else:
                flash('Error analyzing image. Please try again.', 'error')
                return redirect(request.url)
                
        except Exception as e:
            app.logger.error(f"Error processing upload: {str(e)}")
            flash('An error occurred while processing your image. Please try again.', 'error')
            return redirect(request.url)

    return render_template('upload.html')

@app.route('/history')
def history():
    """Display prediction history."""
    try:
        conn = get_db()
        c = conn.cursor()
        predictions = c.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 10').fetchall()
        
        # Convert Row objects to dictionaries and handle timestamp conversion
        predictions_list = []
        for pred in predictions:
            pred_dict = dict(pred)
            if isinstance(pred_dict['timestamp'], str):
                pred_dict['timestamp'] = datetime.strptime(pred_dict['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            # Ensure consistent venom status
            pred_dict['result'] = get_venom_status(pred_dict['is_venomous'])
            predictions_list.append(pred_dict)
        
        conn.close()
        return render_template('history.html', predictions=predictions_list)
    except Exception as e:
        app.logger.error(f"Error fetching history: {str(e)}")
        flash('Error loading prediction history', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
