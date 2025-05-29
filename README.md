# Venomous Creature Detection System

A lightweight web application for detecting potentially venomous creatures using AI, optimized for Raspberry Pi.

## Features
- Real-time image analysis
- Mobile-friendly web interface
- Optimized for Raspberry Pi performance
- Local processing (no internet required after initial setup)

## Requirements
- Raspberry Pi (3B+ or newer recommended)
- Python 3.7 or newer
- At least 1GB of free RAM
- Internet connection for initial setup

## Installation

1. Update system packages:
```bash
sudo apt-get update
sudo apt-get upgrade
```

2. Install system dependencies:
```bash
sudo apt-get install python3-pip python3-dev
```

3. Clone this repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

4. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

## Running the Application

1. Start the web server:
```bash
python3 app.py
```

2. Access the web interface:
- Open a web browser
- Go to: `http://YOUR_RASPBERRY_PI_IP:5000`

## Performance Optimization

If you experience memory issues, you can increase swap space:
```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change CONF_SWAPSIZE to 2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## Troubleshooting

1. If you get memory errors:
   - Increase swap space as shown above
   - Close other applications
   - Restart the Raspberry Pi

2. If the model fails to load:
   - Check internet connection
   - Ensure you have enough free disk space
   - Try running with sudo if permission issues occur

## License
MIT License

# 🐍 NoVenom AI-Powered Venomous Creature Detection

**NoVenom** is a lightweight AI-based web application that helps users identify whether an insect or small animal is venomous - just by uploading a photo. Designed to run on a **Raspberry Pi**, it uses the **Hugging Face Inference API** to process images in the cloud and return accurate classifications in real time.

---

## 🌐 Live Like a Naturalist, Think Like a Scientist

Whether you're out in the field or examining a backyard critter, NoVenom helps you stay informed and safe without needing a biology degree.

---

## 🧠 Core Features

- 🌿 Upload a photo of any insect or small creature
- 🧬 Uses Hugging Face AI models to determine if it's venomous
- ⚡ Fast and efficient: Raspberry Pi sends data, Hugging Face does the heavy lifting
- 🌐 Simple Flask web interface accessible from any browser on the local network

---

## 🛠 Tech Stack

- **Hardware**: Raspberry Pi 3/4 or newer  
- **Backend**: Python + Flask  
- **AI**: Hugging Face transformer  
- **Frontend**: HTML (Jinja2 templating)


