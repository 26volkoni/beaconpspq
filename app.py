import os
import random
import math
from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__)


image_positions = {
    1: (4682,3802),
    2: (180, 220),
    3: (300, 60),
    4: (90, 170),
    5: (210, 90),
    6: (400, 300),
    7: (150, 250),
    8: (350, 200),
    9: (500, 400),
    10: (600, 500),
    11: (700, 600),
    12: (800, 700),
    13: (900, 800),
    14: (1000, 900),
    15: (1100, 1000)
}

@app.route('/')
def index():
    cache_buster = random.randint(1000, 9999)
    return render_template('index.html', cache_buster=cache_buster)

@app.route('/next')
def next_image():
    image_id = random.choice(list(image_positions.keys()))
    image_filename = f"{image_id}.png"
    return jsonify({
        "image": image_filename,
        "image_id": image_id
    })

@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    image_id = int(data['image_id'])
    guess_x = int(data['x'])
    guess_y = int(data['y'])

    if image_id not in image_positions:
        return jsonify({"error": "Invalid image ID"}), 400

    true_x, true_y = image_positions[image_id]
    distance = math.sqrt((true_x - guess_x)**2 + (true_y - guess_y)**2)
    score = max(0, int(100 - distance))

    return jsonify({
        "distance": int(distance),
        "score": score
    })
