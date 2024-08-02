"""
API Endpoint definition for frame object detection.

Author: Aryaman Pandya
"""

import os

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from object_detection_web_service.detection_service.detection_core import run_detection

app = Flask(__name__)


@app.route("/process", methods=["POST"])
def handle_object_detection_request():
    """
    Process the uploaded frame for object detection.

    This endpoint expects a POST request with frame paths in the 'frame' field.
    It runs object detection on the provided frame and returns the results.

    Args:
        None
    Returns:
        JSON response with detection results or error message.
    """
    if "frame" not in request.files:
        return jsonify({"error": "No frame file"}), 400

    frame = request.files["frame"]
    if frame.filename == "":
        return jsonify({"error": "No selected frame"}), 400

    if frame:
        # Save the file temporarily, process, then evict
        filename = secure_filename(frame.filename)
        temp_path = os.path.join("/tmp", filename)
        frame.save(temp_path)
        result = run_detection(temp_path, False)
        os.remove(temp_path)

        return result

    return jsonify({"error": "Unknown"}), 500


if __name__ == "__main__":
    app.run(debug=True)
