from flask import Flask, render_template, jsonify
from motion_detection import motionDetection
import threading

from flask import Flask, render_template, jsonify
from motion_detection import motionDetection
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-motion-detection')
def start_motion_detection():
    # DO NOT use daemon thread
    t = threading.Thread(target=motionDetection)
    t.start()

    return jsonify(message='Human motion detection started. Press ESC to stop.')

if __name__ == "__main__":
    # Disable auto reloader
    app.run(debug=False, use_reloader=False)

