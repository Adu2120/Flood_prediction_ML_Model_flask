# encoding: utf-8
import json
from flask import Flask, request, jsonify, send_from_directory
import model as model 
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hiii():
    return "Hello"

# @app.route('/favicon.ico') 
# def favicon(): 
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'veloce-Icon_WHITE.png', mimetype='image/vnd.microsoft.icon')

@app.route('/predict', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    output = model.predict_wf_wl(record['nitawade_wl'], record['nitawade_wf'], record['balinge_wl'], record['balinge_wf'])
    return jsonify(output)

app.run()
