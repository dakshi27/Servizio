from flask import Flask, render_template, request, redirect, url_for, session, flash
import cv2
import face_recognition
import numpy as np
import os

# Import Blueprints
from services.keyword_finder import keyword_finder_bp
from services.text_summarizer import text_summarizer_bp  # Text Summarizer Import
from services.image_finder.image_finder import image_finder_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users = {}

# Register Blueprints
app.register_blueprint(keyword_finder_bp, url_prefix='/keyword_finder')
app.register_blueprint(text_summarizer_bp, url_prefix='/text_summarizer')  # Register Text Summarizer Blueprint
app.register_blueprint(image_finder_bp,url_prefix='/image_finder')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            flash("User already exists. Please login.", "warning")
            return redirect(url_for('login'))

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            flash("Failed to capture image. Try again.", "danger")
            return redirect(url_for('signup'))

        face_encodings = face_recognition.face_encodings(frame)
        if len(face_encodings) == 0:
            flash("No face detected. Try again.", "danger")
            return redirect(url_for('signup'))

        users[username] = face_encodings[0]
        flash("Signup successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html', base_template='base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username not in users:
            flash("User not found. Please sign up first.", "warning")
            return redirect(url_for('signup'))

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            flash("Failed to capture image. Try again.", "danger")
            return redirect(url_for('login'))

        face_encodings = face_recognition.face_encodings(frame)
        if len(face_encodings) == 0:
            flash("No face detected. Try again.", "danger")
            return redirect(url_for('login'))

        stored_encoding = users[username]

        match = face_recognition.compare_faces([stored_encoding], face_encodings[0], tolerance=0.45)
        face_distance = face_recognition.face_distance([stored_encoding], face_encodings[0])[0]

        if match[0] and face_distance < 0.40:
            session['user'] = username
            flash(f"Welcome, {username}! You have successfully logged in.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Face did not match. Try again.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', base_template='base.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['user'], base_template='base.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
