# NoVenom 🕷️

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-2.x-38B2AC.svg)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57.svg)](https://www.sqlite.org/)

>  AI-powered web application for venom detection and species identification.

## 📋 Overview

NoVenom is a Flask-based web application that leverages artificial intelligence to analyze images of creatures and determine their venom status. The application features a modern, responsive interface and maintains a comprehensive history of predictions.

## ✨ Core Features

### 🔍 Image Analysis
- Real-time AI-powered image processing
- Venom status detection
- Species identification
- Confidence scoring

### 🎨 User Interface
- Intuitive photo upload
- Responsive design for all devices
- Real-time progress indicators
- Clean, professional results display

### 💾 Data Management
- Secure image storage
- Prediction history tracking
- SQLite database integration
- Unique file naming system

## 🏗️ Technical Architecture

### Backend Components
| Component | Technology |
|-----------|------------|
| Web Framework | Flask |
| Database | SQLite |
| File Handling | Werkzeug |
| API Communication | Requests |

### Frontend Implementation
| Component | Technology |
|-----------|------------|
| Framework | Tailwind CSS |
| Icons | Font Awesome |
| Templates | Jinja2 |
| Interactivity | Vanilla JavaScript |

### AI Integration
| Component | Technology |
|-----------|------------|
| Model | ResNet-50 |
| Framework | PyTorch |
| Library | Hugging Face Transformers |

## ⚙️ System Requirements

- Python 3.x
- Modern web browser
- Internet connection
- 500MB free disk space

## 🚀 Installation

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Initialization**
   ```bash
   python init_db.py
   ```

## ⚡ Configuration

### AI Server
```python
AI_SERVER_URL = "http://your-ai-server:5001/analyze"
```

### File Storage
```python
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
```

## 📁 Application Structure

```
novenom/
├── app.py              # Flask application
├── ai_server.py        # AI model server
├── requirements.txt    # Dependencies
├── requirements_pi.txt # For Raspberry Pi
├── static/
│   ├── css/           # Stylesheets
│   └── uploads/       # Image storage
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   └── history.html
└── novenom.db        # Database
```

## 📖 Usage Guide

### 1. Image Upload
- Navigate to the upload page
- Select or drag an image
- Wait for processing

### 2. Results View
- Venom status indicator
- Species identification
- Confidence metrics
- Historical data access

## 🆘 Support

For technical support or inquiries, please contact the development team.

## 📦 Dependencies

- Flask
- PyTorch
- Transformers
- SQLite3
- Tailwind CSS
- Font Awesome

---

<div align="center">
Made with ❤️ by the NoVenom Team
</div>


