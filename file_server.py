from flask import Flask, send_from_directory
import os

app = Flask(__name__)
SERVER_FOLDER = os.path.join(os.path.dirname(__file__), "server_files")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(SERVER_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
