from flask import Flask, render_template, request, jsonify
import os
import random
import json
import math
import time
 
app = Flask(__name__)
 
with open("locations.json") as f:
    locations = json.load(f)
 
@app.route('/')
def index():
    location = random.choice(locations)
    image_id = locations.index(location)
    cache_buster = int(time.time() * 1000)  # unique number each time
    return render_template('index.html', location=location, image_id=image_id, cache_buster=cache_buster)
 
@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    image_id = int(data['image_id'])
    guess_x = data['x']
    guess_y = data['y']
 
    correct = locations[image_id]['answer']
    dx = guess_x - correct['x']
    dy = guess_y - correct['y']
    distance = round(math.sqrt(dx*dx + dy*dy))
 
    return jsonify({'distance': distance})
 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)