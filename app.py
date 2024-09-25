import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from music21 import converter, stream
from pdf2image import convert_from_path
from core.music_analysis import analyze_music
from core.sheet_modifier import modify_sheet_music
from config import get_config

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment (development/production/testing)
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(get_config(env))

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Allowed extensions for sheet music uploads
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']


# Function to check if the uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')


# Route to handle file uploads and sheet music analysis
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Determine skill level from the form input
        skill_level = request.form.get('skill_level')

        # Process the file and recommend fingerings
        try:
            result_file = process_sheet_music(filepath, filename, skill_level)
            flash(f'File processed successfully! Download the modified sheet music with finger positions.')
            return send_from_directory(app.config['UPLOAD_FOLDER'], result_file, as_attachment=True)
        except Exception as e:
            flash(f'Error processing the file: {str(e)}')
            return redirect(url_for('home'))

    flash('Invalid file format. Please upload a valid PDF, JPG, or MusicXML file.')
    return redirect(url_for('home'))


# Function to process the uploaded sheet music
def process_sheet_music(filepath, filename, skill_level):
    # Determine the file extension
    file_ext = filename.rsplit('.', 1)[1].lower()

    if file_ext in ['pdf', 'jpg', 'jpeg']:
        # Process PDF or Image files using Tesseract OCR
        return process_image_or_pdf(filepath, skill_level)
    elif file_ext in ['xml', 'musicxml']:
        # Process MusicXML files
        return process_musicxml(filepath, skill_level)
    else:
        raise ValueError('Unsupported file format')


# Process image or PDF files using Tesseract OCR
def process_image_or_pdf(filepath, skill_level):
    if filepath.endswith('.pdf'):
        # Convert PDF to images
        images = convert_from_path(filepath)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
    else:
        # Process image files directly
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)

    # Analyze the text and recommend fingerings
    fingerings = analyze_music(text, skill_level)

    # Modify the sheet music with the recommended fingerings
    modified_filepath = modify_sheet_music(filepath, fingerings)

    return modified_filepath


# Process MusicXML files
def process_musicxml(filepath, skill_level):
    # Use music21 to analyze MusicXML files
    music_score = converter.parse(filepath)

    # Analyze and recommend fingerings
    fingerings = analyze_music(music_score, skill_level)

    # Modify the MusicXML file with the recommended fingerings
    modified_filepath = modify_sheet_music(filepath, fingerings)

    return modified_filepath


# Error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Error handler for 500 errors
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])

