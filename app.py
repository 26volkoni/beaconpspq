from flask import Flask, render_template
import os
import random
import json

app = Flask(__name__)
@app.route('/')
def index():
    with open("locations.json") as f:
        locations = json.load(f)
    location = random.choice(locations)
    return render_template('index.html', location=location, image_id=locations.index(location))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)