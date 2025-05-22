from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from huggingface_hub import InferenceClient  
import json  
import traceback 

# 여기에 본인의 예측 함수 import
# from your_model_module import model_predict

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    error = None
    image_url = None
    result = None

    if request.method == 'POST':
        # Check file part
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

                # === 모델 예측 호출 ===
                # is_safe = model_predict(filepath)
                # result = "안전합니다 ✅" if is_safe else "안전하지 않습니다 ⚠️"
                # === 예시 ===
                # 임시로 랜덤 결과
                import random
                is_safe = random.choice([True, False])
                result = "Safe ✅" if is_safe else "Unsafe ⚠️"
                # =======================

            else:
                error = 'File type not allowed'

    return render_template('upload.html',
                           error=error,
                           image_url=image_url,
                           result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
