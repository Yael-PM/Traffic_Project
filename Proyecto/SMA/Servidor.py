from flask import Flask, jsonify
import json, logging, os
from model import BoidFlockers

port = 8000
app = Flask(__name__, static_url_path='')

boids = BoidFlockers(
    20,
    100,
    100,
    1,
    10,
    2,
    0.03,
    0.015,
    0.05
)

@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify([{'message': 'Hello, World!'}])

@app.route('/datos', methods=['GET', 'POST'])
def getPositions():
    boids.step()
    pos=boids.getPositions()

    p = []
    for po in pos:
        Point = {'x': po[0], 'y': po[1]}
        p.append(Point)
    return jsonify({'points': p})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)
