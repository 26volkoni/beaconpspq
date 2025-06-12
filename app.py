import os
import random
import math
from flask import Flask, render_template, jsonify, request, send_from_directory, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')

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

def calculate_score(distance):
    if distance < 20:
        return 100
    elif distance < 50:
        return 75
    elif distance < 100:
        return 50
    elif distance < 150:
        return 25
    elif distance < 200:
        return 10
    else:
        return 0

@app.route('/')
def index():
    session.clear()
    cache_buster = random.randint(1000, 9999)
    return render_template('index.html', cache_buster=cache_buster)

@app.route('/next')
def next_image():
    used = session.get('used_images', [])
    all_ids = list(image_positions.keys())
    available = [i for i in all_ids if i not in used]
    if not available:
        return jsonify({'end': True})
    image_id = random.choice(available)
    used.append(image_id)
    session['used_images'] = used
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
    score = calculate_score(distance)
    scores = session.get('scores', [])
    scores.append(score)
    session['scores'] = scores
    total_score = sum(scores)
    return jsonify({
        "distance": int(distance),
        "score": score,
        "total_score": total_score,
        "round": len(scores)
    })

@app.route('/restart', methods=['POST'])
def restart():
    session.clear()
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
