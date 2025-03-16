from flask import Blueprint, request, render_template, session, flash, redirect, url_for
import os
import docx

keyword_finder_bp = Blueprint('keyword_finder', __name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@keyword_finder_bp.route('/', methods=['GET', 'POST'])
def keyword_finder():
    found_lines = []  # Default empty results

    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file selected!", "danger")
            return redirect(url_for('keyword_finder.keyword_finder'))

        file = request.files['file']
        keyword = request.form['keyword'].strip().lower()

        if not keyword:
            flash("Please enter a keyword!", "danger")
            return redirect(url_for('keyword_finder.keyword_finder'))

        if file.filename == '':
            flash("No file uploaded!", "danger")
            return redirect(url_for('keyword_finder.keyword_finder'))

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        try:
            if file.filename.endswith('.txt'):
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                found_lines = [
                    f"Line {i+1}: {line.strip()}"
                    for i, line in enumerate(lines)
                    if keyword in line.lower()
                ]

            elif file.filename.endswith('.docx'):
                doc = docx.Document(file_path)
                lines = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
                found_lines = [
                    f"Paragraph {i+1}: {line}"
                    for i, line in enumerate(lines)
                    if keyword in line.lower()
                ]

            else:
                flash("Unsupported file format! Please upload a .txt or .docx file.", "danger")
                return redirect(url_for('keyword_finder.keyword_finder'))

        except Exception as e:
            flash(f"Error reading file: {str(e)}", "danger")
            return redirect(url_for('keyword_finder.keyword_finder'))

    return render_template('keyword_finder.html', results=found_lines)
