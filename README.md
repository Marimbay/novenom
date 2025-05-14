# 🐍 NoVenom — AI-Powered Venomous Creature Detection

**NoVenom** is a lightweight AI-based web application that helps users identify whether an insect or small animal is venomous - just by uploading a photo. Designed to run on a **Raspberry Pi**, it uses the **Hugging Face Inference API** to process images in the cloud and return accurate classifications in real time.

---

## 🌐 Live Like a Naturalist, Think Like a Scientist

Whether you're out in the field or examining a backyard critter, NoVenom helps you stay informed and safe without needing a biology degree.

---

## 🧠 Core Features

- 🌿 Upload a photo of any insect or small creature
- 🧬 Uses Hugging Face AI models to determine if it’s venomous
- ⚡ Fast and efficient: Raspberry Pi sends data, Hugging Face does the heavy lifting
- 🌐 Simple Flask web interface accessible from any browser on the local network

---

## 🛠 Tech Stack

- **Hardware**: Raspberry Pi 3/4 or newer  
- **Backend**: Python + Flask  
- **AI**: Hugging Face Inference API  
- **Frontend**: HTML (Jinja2 templating)


🐍 NoVenom Project — Required Files and Components (in English)
1. Flask Web Server File (Python)
File: app.py

Purpose:

Launch a web server using Flask

Handle photo uploads through an HTML form

Send the uploaded image to the Hugging Face Inference API

Display the classification result back to the user

Key Points:

Using Flask modules (flask, flask_uploads, flask_render_template, etc.)

Understanding GET/POST methods

Handling file saving and reading

Communicating with external APIs using requests

2. HTML Template File
File: templates/index.html

Purpose:

Provide a simple user interface for uploading photos

Display the classification result

Key Points:

Basic HTML structure

Using Jinja2 template syntax in Flask ({{ result }})

Form setup for file upload (<form enctype="multipart/form-data">)

3. Python Requirements File
File: requirements.txt

Purpose:

List of all Python packages required to run the project

Typical contents:

txt
Copy
Edit
Flask
requests
gunicorn (optional, for deployment)
Key Points:

Allows easy setup by running pip install -r requirements.txt

4. Raspberry Pi Environment Setup
Component: Raspberry Pi device configuration

Purpose:

Install Python and necessary libraries

Deploy and run the NoVenom project on Raspberry Pi

Allow access to the Flask server over the local network

Key Points:

Bind the Flask server to 0.0.0.0 to allow external devices to connect

5. Hugging Face Inference API Setup
Component: Hugging Face API Token and Setup

Purpose:

Sign up on Hugging Face

Obtain an API Key (Token)

Integrate the Token into the Python code to authenticate API requests

Key Points:

Be aware of the free-tier usage limits

Choose an appropriate AI model for venomous creature detection

