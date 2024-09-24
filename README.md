# CelloFingers

CelloFingers is a Python web application designed to analyze cello sheet music and provide optimal fingering positions for the best playing experience. Whether you are a beginner, intermediate, or advanced cellist, CelloFingers will recommend finger positions based on your skill level and even modify the sheet music if possible. The application supports various sheet music formats such as PDF, JPG, and MusicXML.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [Folder Structure](#folder-structure)
6. [Author](#author)
7. [Contributing](#contributing)

## Features

- Analyze uploaded cello sheet music (PDF, JPG, MusicXML).
- Recommend fingering positions for three skill levels:
  - Beginner
  - Intermediate
  - Advanced
- Modify sheet music with recommended finger positions (if format supports).
- Alert users if the modification is not possible and provide manual finger positions.
- Web-based interface for easy interaction.

## Technologies Used

- **Python**: Core programming language
- **Flask**: Backend framework to develop the web-based interface
- **Pillow**: Image manipulation for JPG/PDF handling
- **Music21**: Python toolkit for analyzing and modifying MusicXML files
- **pdf2image**: Convert PDF sheets to image format for analysis
- **Tesseract**: OCR to read JPG sheet music
- **OpenCV**: Image processing for finger position overlays on sheet music
- **JavaScript**: Frontend interactivity for file upload and user input
- **HTML/CSS**: Web page structure and design
- **Bootstrap**: Frontend framework for responsive design

## Setup and Installation

### Prerequisites

- Python 3.10+
- PIP (Python package installer)
- PyCharm Pro (recommended, but any IDE will work)
- Tesseract OCR (for image-based sheet music recognition)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/liquidmonks/CelloFingers.git
   cd CelloFingers
   ```
2. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
3. Install required dependencies:
   pip install -r requirements.txt
4. Set up Tesseract OCR:
   Download and install Tesseract from here.
   Add Tesseract to your system's PATH.
5. Run the application locally:
   flask run
6. Open your web browser and go to http://localhost:5000 to access the web interface.

## Usage

Upload your sheet music file (PDF, JPG, or MusicXML).
Select your skill level (Beginner, Intermediate, Advanced).
The application will analyze the music and either:
Automatically add the recommended fingering positions to your sheet music, or
Provide a set of recommended fingering positions to manually add if the automatic modification is not possible.
Download or review the modified sheet music.

## Folder Structure

CelloFingers/
│
├── app/
│   ├── static/
│   │   ├── css/           # CSS files for the web interface
│   │   ├── js/            # JavaScript files for client-side interactivity
│   └── templates/         # HTML files for the web interface
│
├── core/
│   ├── music_analysis.py   # Logic for analyzing music and generating fingerings
│   ├── sheet_modifier.py   # Logic for modifying the sheet music
│   └── ocr_processing.py   # Logic for handling JPG/PDF OCR using Tesseract
│
├── uploads/                # Temporary storage for uploaded sheet music
│
├── tests/                  # Unit tests for various components
│
├── requirements.txt        # Python dependencies
├── app.py                  # Entry point of the Flask application
└── README.md               # Project documentation

## Author

Created by Liquid Monks
GitHub Profile: Liquid Monks

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions, bug fixes, or new features.

5. Workflow and Setup Tips

### 

* **Git Commits:** To keep track of changes, I recommend committing small changes as follows:
  * `git add <file>`: Add files to the staging area.
  * `git commit -m "Short description of what you changed"`: Commit the change.
  * `git push`: Push the changes to your GitHub repository.
