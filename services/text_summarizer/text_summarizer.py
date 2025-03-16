from flask import Blueprint, request, render_template, session, flash, redirect, url_for
import os
import PyPDF2
import docx
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

text_summarizer_bp = Blueprint('text_summarizer', __name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@text_summarizer_bp.route('/', methods=['GET', 'POST'])
def text_summarizer():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file selected!", "danger")
            return redirect(url_for('text_summarizer.text_summarizer'))

        file = request.files['file']
        if file.filename == '':
            flash("No file uploaded!", "danger")
            return redirect(url_for('text_summarizer.text_summarizer'))

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        extracted_text = extract_text(file_path)
        if not extracted_text:
            flash("Could not extract text from file!", "danger")
            return redirect(url_for('text_summarizer.text_summarizer'))

        summary = summarize_text(extracted_text)

        return render_template('text_summarizer.html', summary=summary)

    return render_template('text_summarizer.html')

def extract_text(file_path):
    """Extracts text from a PDF, DOCX, or TXT file."""
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            return " ".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
        
        elif file_path.endswith('.txt'):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def summarize_text(text):
    """Summarizes the extracted text using Sumy (LSA)."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)  # Return 3 summarized sentences
    return " ".join(str(sentence) for sentence in summary)
