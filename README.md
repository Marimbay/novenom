# NoVenom - AI-Powered Venom Detection

NoVenom is a web application that uses artificial intelligence to detect and identify potentially venomous creatures from uploaded images. The application provides instant analysis and maintains a history of predictions for reference.

## Features

- 🖼️ **Image Upload**: Drag-and-drop or file selection interface for easy image uploads
- 🤖 **AI Analysis**: Real-time analysis of uploaded images using a pre-trained ResNet-50 model
- 🎯 **Venom Detection**: Identifies whether the creature in the image is venomous
- 📊 **Confidence Scoring**: Shows the confidence level of each prediction
- 📝 **Species Identification**: Identifies and displays the species name in a clean, professional format
- 📱 **Responsive Design**: Modern UI that works seamlessly on both desktop and mobile devices
- 📚 **Prediction History**: Maintains a history of previous predictions with detailed information
- 🔒 **Secure Storage**: Unique file naming and secure storage of uploaded images

## Tech Stack

### Backend
- **Python 3.x**: Core programming language
- **Flask**: Web framework
- **SQLite**: Database for storing prediction history
- **Requests**: HTTP library for API communication
- **Werkzeug**: File handling and security utilities

### Frontend
- **HTML5**: Structure
- **Tailwind CSS**: Utility-first CSS framework for styling
- **JavaScript**: Client-side interactivity
- **Font Awesome**: Icon library

### AI/ML
- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face's library for state-of-the-art NLP
- **ResNet-50**: Pre-trained model for image classification

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Modern web browser
- Internet connection

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/novenom.git
   cd novenom
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python init_db.py
   ```

## Configuration

1. Update the AI server URL in `app.py`:
   ```python
   AI_SERVER_URL = "http://your-ai-server:5001/analyze"
   ```

2. Configure the upload folder path if needed:
   ```python
   UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
   ```

## Running the Application

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Access the application in your web browser:
   ```
   http://localhost:5000
   ```

## Project Structure

```
novenom/
├── app.py              # Main Flask application
├── ai_server.py        # AI model server
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/           # CSS files
│   └── uploads/       # Uploaded images
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   └── history.html
└── novenom.db        # SQLite database
```

## Usage

1. Navigate to the upload page
2. Upload an image of a creature
3. Wait for the AI analysis
4. View the results:
   - Venom status
   - Identified species
   - Confidence level
5. Check the history page for past predictions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for the Transformers library
- Flask team for the web framework
- Tailwind CSS team for the styling framework


