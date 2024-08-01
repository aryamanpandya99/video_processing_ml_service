"""
API Endpoint definition for frame object detection.

Author: Aryaman Pandya
"""
import os
from werkzeug.utils import secure_filename

from flask import Flask, jsonify, request
from object_detection_web_service.detection_service.detection_core import run_detection

app = Flask(__name__)

from flask import request, jsonify

@app.route("/process", methods=["POST"])
def process():
    """
    Process the uploaded frame for object detection.

    This endpoint expects a POST request with frame paths in the 'frame' field.
    It runs object detection on the provided frame and returns the results.

    Returns:
        JSON response with detection results or error message.
        200 - Successful detection
        400 - Bad request (missing frame or empty frame name)
    """
    if "frame" not in request.files:
        return jsonify({"error": "No frame file"}), 400

    frame = request.files["frame"]
    if frame.filename == "":
        return jsonify({"error": "No selected frame"}), 400

    if frame:
        # Save the file temporarily
        filename = secure_filename(frame.filename)
        temp_path = os.path.join('/tmp', filename)
        frame.save(temp_path)
        
        # Run detection on the saved file
        result = run_detection(temp_path, False)
        
        # Remove the temporary file
        os.remove(temp_path)
        
        return result

    return jsonify({"error": "Unknown"}), 500