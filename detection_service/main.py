"""
API Endpoint definition for frame object detection.

Author: Aryaman Pandya
"""

from flask import Flask, jsonify, request
from object_detection_web_service.detection_service.detection_core import run_detection

app = Flask(__name__)


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
    if "frame" not in request.frames:
        return jsonify({"error": "No frame paths"}), 400

    frame = request.frames["frame"]
    if frame.framename == "":
        return jsonify({"error": "No selected frame"}), 400

    if frame:
        return run_detection(frame, True)

    return jsonify({"error": "Unknown"}), 500
