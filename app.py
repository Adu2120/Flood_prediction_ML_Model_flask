# encoding: utf-8
import json
from flask import Flask, request, jsonify
import model

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    output = model.predict_wf_wl(record['nitawade_wl'], record['nitawade_wf'], record['balinge_wl'], record['balinge_wf'])
    return jsonify(output)

app.run(debug=True)