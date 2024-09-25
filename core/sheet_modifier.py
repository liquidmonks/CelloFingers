from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path  # Correct import for PDF to image conversion
from music21 import converter  # Correct import for MusicXML handling


# Function to modify sheet music with fingerings
def modify_sheet_music(filepath, fingerings):
    """
    Modifies the sheet music with the recommended finger positions.

    :param filepath: Path to the uploaded sheet music file (either image or MusicXML).
    :param fingerings: A dictionary of recommended fingerings for each note.
    :return: Path to the modified sheet music file.
    """

    if filepath.endswith('.jpg') or filepath.endswith('.jpeg') or filepath.endswith('.png'):
        return modify_image(filepath, fingerings)
    elif filepath.endswith('.pdf'):
        return modify_pdf(filepath, fingerings)  # Modify the PDF by converting it to images
    elif filepath.endswith('.xml') or filepath.endswith('.musicxml'):
        return modify_musicxml(filepath, fingerings)
    else:
        raise ValueError('Unsupported file format')


def modify_image(image_path, fingerings):
    """
    Adds finger positions to an image file (e.g., JPG, PNG).

    :param image_path: Path to the image file.
    :param fingerings: A dictionary of recommended fingerings for each note.
    :return: Path to the modified image file.
    """

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Load a font for the fingerings overlay
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Example: Add fingering text at arbitrary positions
    position = (50, 50)
    for note, fingering in fingerings.items():
        draw.text(position, f"{note}: {fingering}", fill="black", font=font)
        position = (position[0], position[1] + 30)  # Move the text down for the next note

    modified_path = image_path.replace(".", "_modified.")
    img.save(modified_path)

    return modified_path


def modify_pdf(pdf_path, fingerings):
    """
    Converts a PDF to images, adds finger positions, and converts back to a PDF.

    :param pdf_path: Path to the PDF file.
    :param fingerings: A dictionary of recommended fingerings for each note.
    :return: Path to the modified PDF file.
    """
    # Convert PDF to images
    images = convert_from_path(pdf_path)

    modified_images = []
    for img in images:
        draw = ImageDraw.Draw(img)
        position = (50, 50)
        for note, fingering in fingerings.items():
            draw.text(position, f"{note}: {fingering}", fill="black")
            position = (position[0], position[1] + 30)
        modified_images.append(img)

    modified_pdf_path = pdf_path.replace(".", "_modified.")
    modified_images[0].save(modified_pdf_path, save_all=True, append_images=modified_images[1:])

    return modified_pdf_path


def modify_musicxml(xml_path, fingerings):
    """
    Adds finger positions to a MusicXML file.

    :param xml_path: Path to the MusicXML file.
    :param fingerings: A dictionary of recommended fingerings for each note.
    :return: Path to the modified MusicXML file.
    """
    score = converter.parse(xml_path)

    # Example of adding fingerings as text annotations
    for element in score.flat.notes:
        if element.nameWithOctave in fingerings:
            fingering = fingerings[element.nameWithOctave]
            element.addLyric(f"Fingering: {fingering}")

    modified_xml_path = xml_path.replace(".", "_modified.")
    score.write('musicxml', modified_xml_path)

    return modified_xml_path
