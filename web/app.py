from flask import Flask, request, send_file, render_template, redirect, jsonify
import os
import uuid
import subprocess

app = Flask(__name__)
UPLOAD_DIR = "/tmp/pdf2pro6x"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "Datei ist zu groß. Maximal 2 GB erlaubt."}), 413

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "Keine Datei hochgeladen."}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Keine Datei ausgewählt."}), 400
        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Nur PDF-Dateien sind erlaubt."}), 400

        original_name = os.path.splitext(file.filename)[0]
        input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{original_name}.pdf")
        output_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{original_name}.pro6x")

        try:
            file.save(input_path)
            process = subprocess.run([
                "../venv/bin/python", "converter.py",
                input_path, output_path
            ], capture_output=True, timeout=60)

            if process.returncode != 0:
                return jsonify({"error": "Fehler bei der Konvertierung. Datei ungültig oder defekt."}), 422

            return send_file(output_path, as_attachment=True, download_name=f"{original_name}.pro6x")

        except subprocess.TimeoutExpired:
            return jsonify({"error": "Die Konvertierung hat zu lange gedauert."}), 504
        except Exception as e:
            return jsonify({"error": "Unerwarteter Fehler beim Verarbeiten der Datei."}), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8808)
