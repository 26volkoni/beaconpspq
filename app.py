import os
import random
import math
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


ORIGINAL_MAP_WIDTH = 6250
ORIGINAL_MAP_HEIGHT = 4419
DISPLAYED_MAP_WIDTH = 700  

image_positions = {
    1: (524, 426),
    2: (168, 278),
    3: (166, 281),
    4: (387, 373),
    5: (378, 384),
    6: (395, 391),
    7: (398, 388),
    8: (386, 402),
    9: (397, 403),
    10: (391, 399),
    11: (391, 399),
    12: (155, 170),
    13: (172, 192),
    14: (171, 166),
    15: (161, 156),
    16: (167, 191),
    17: (166, 198),
    18: (171, 228),
    19: (169,232),
    20: (165,233),
    21: (169,220),
    22: (172,238),
    23: (164,242),
    24: (166,241),
    25: (140,251),
    26: (130,250),
    27: (138,243),
    28: (53,229),
    29: (117,241),
    30: (120,230),
    31: (97,226),
}

def calculate_score(distance):
    if distance < 55:  # was 50
        return 100
    elif distance < 110:  # was 100
        return 90
    elif distance < 220:  # was 200
        return 75
    elif distance < 440:  # was 400
        return 50
    elif distance < 770:  # was 700
        return 25
    else:
        return 0

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
        return jsonify({'distance': -1, 'score': 0, 'error': 'Invalid image_id'})

    correct_x, correct_y = image_positions[image_id]

    # Remove scaling: both guess and answer are in minimap/displayed coordinates
    dx = guess_x - correct_x
    dy = guess_y - correct_y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    score = calculate_score(distance)

    return jsonify({
        'distance': round(distance),
        'score': score,
        'max_score': 100,
        'message': f"You scored {score} out of 100!"
    })

@app.route('/debug_coords/<int:image_id>')
def debug_coords(image_id):
    if image_id in image_positions:
        return jsonify({
            'image_id': image_id,
            'coordinates': image_positions[image_id]
        })
    return jsonify({'error': 'Image ID not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
