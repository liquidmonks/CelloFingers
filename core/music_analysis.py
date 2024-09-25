import re
from music21 import note, chord, stream


# Developer Comments:
# This function analyzes the content of the sheet music (either plain text from OCR or parsed MusicXML)
# and generates recommended finger positions based on the user's skill level.

def analyze_music(sheet_content, skill_level):
    """
    Analyzes the sheet music content and recommends finger positions based on skill level.

    :param sheet_content: The content of the sheet music, can be text from OCR or a music21 stream object.
    :param skill_level: The user's skill level ('beginner', 'intermediate', 'advanced').
    :return: A dictionary of note positions and their recommended fingerings.
    """

    # This will store the recommended fingerings for each note or chord
    recommended_fingerings = {}

    if isinstance(sheet_content, str):
        # If the sheet_content is a string (i.e., text from OCR), we need to parse it
        notes = extract_notes_from_text(sheet_content)
    elif isinstance(sheet_content, stream.Score):
        # If the sheet_content is a music21 stream (i.e., from MusicXML), we extract notes
        notes = extract_notes_from_stream(sheet_content)
    else:
        raise ValueError('Unsupported sheet content format')

    # Analyze each note/chord and recommend fingerings based on skill level
    for element in notes:
        if isinstance(element, note.Note):
            recommended_fingerings[element.nameWithOctave] = get_fingering_for_note(element, skill_level)
        elif isinstance(element, chord.Chord):
            chord_fingerings = [get_fingering_for_note(n, skill_level) for n in element.notes]
            recommended_fingerings[element.fullName] = chord_fingerings

    return recommended_fingerings


def extract_notes_from_text(text):
    """
    Extracts notes from OCR-processed text. This is a simplified example that assumes note names
    are written in the text (e.g., C4, D5, etc.).

    :param text: The raw text from OCR processing.
    :return: A list of music21 note objects.
    """
    note_pattern = r'[A-Ga-g][#b]?\d'  # Matches notes like C4, D#5, Bb3
    matches = re.findall(note_pattern, text)

    notes = []
    for match in matches:
        try:
            n = note.Note(match)
            notes.append(n)
        except Exception as e:
            # Handle any note parsing errors
            print(f"Error parsing note: {match} -> {e}")
    return notes


def extract_notes_from_stream(music_stream):
    """
    Extracts notes from a music21 stream (typically from a MusicXML file).

    :param music_stream: The music21 stream object representing the sheet music.
    :return: A list of note or chord objects.
    """
    return music_stream.flat.notes


def get_fingering_for_note(n, skill_level):
    """
    Returns a recommended fingering for a single note based on the skill level.

    :param n: A music21 note object.
    :param skill_level: The user's skill level ('beginner', 'intermediate', 'advanced').
    :return: A string representing the recommended finger position.
    """

    # Define fingerings for different skill levels
    beginner_fingerings = {1: 'Index finger', 2: 'Middle finger', 3: 'Ring finger', 4: 'Pinky finger'}
    intermediate_fingerings = {1: 'Thumb', 2: 'Index finger', 3: 'Middle finger', 4: 'Ring finger'}
    advanced_fingerings = {1: 'Thumb', 2: 'Index finger', 3: 'Middle finger', 4: 'Pinky finger'}

    # A simplified example based on pitch, adjust based on real fingering rules
    pitch = n.pitch.midi % 4 + 1  # Simple calculation to get a finger (just as an example)

    if skill_level == 'beginner':
        return beginner_fingerings.get(pitch, 'Unknown')
    elif skill_level == 'intermediate':
        return intermediate_fingerings.get(pitch, 'Unknown')
    elif skill_level == 'advanced':
        return advanced_fingerings.get(pitch, 'Unknown')
    else:
        raise ValueError('Unknown skill level')
