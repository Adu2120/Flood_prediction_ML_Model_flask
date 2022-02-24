# encoding: utf-8
import json
from click import password_option
from flask import Flask, request, jsonify, send_from_directory
from numpy import outer
import model as model 
import psycopg2
import psycopg2.extras
import os
from flask_cors import CORS, cross_origin
# from lstm_price_route import lstm_price_blueprint
# from lstm_route import lstm_blueprint

app = Flask(__name__)
cors = CORS(app , resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})
# app.register_blueprint(lstm_blueprint)
# app.register_blueprint(lstm_price_blueprint)

conn = psycopg2.connect(dbname="d7o74rl8ij8n3o", user="zelvoyofzgdudm", password="4caee932563106c232bc134a614f4d13fe49d50991c98867508dfa4be0a185c3", host="ec2-35-153-35-94.compute-1.amazonaws.com")

@app.route('/', methods=['GET'])
def hiii():
    return "Hello"

@app.route('/favicon.ico', methods=['GET']) 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/insert_station', methods=['POST'])
def insert_station():
    record = json.loads(request.data)
    cur = conn.cursor()
    i = "INSERT INTO public.station_details(name, latitude, longitude, district, taluka, waterflow, waterlevel, predicted_wf, predicted_wl, alert) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"    
    data = (record['name'],record['latitude'],record['longitude'],record['district'],record['taluka'],record['waterflow'],record['waterlevel'],record['predicted_wf'],record['predicted_wl'],record['alert'])
    cur.execute(i, data)
    conn.commit()
    return jsonify({})

@app.route('/predict', methods=['POST'])
def update_record():    
    record = json.loads(request.data)
    cur = conn.cursor()
    #insert query of stored Data
    s = "INSERT INTO public.stored_data(water_flow, water_level, station_id) VALUES (%s, %s, %s);"
    ur = "UPDATE station_details SET waterflow = %s, waterlevel = %s, time_stamp=now() where id = %s;"
    up = "UPDATE station_details SET predicted_wf = %s, predicted_wl = %s where id = %s;"
    
    #inserting data of Nitawade
    data = (record['nitawade_wf'], record['nitawade_wl'], 1)
    cur.execute(s, data)
    conn.commit()
    cur.execute(ur, data)
    conn.commit()
    cur.execute(up, data)
    conn.commit()

    #Updating WF and WL Data of Nitawade

    #inserting data of Balinge
    data = (record['balinge_wf'], record['balinge_wl'], 2)
    cur.execute(s, data)
    conn.commit()
    cur.execute(ur, data)
    conn.commit()
    cur.execute(up, data)
    conn.commit()

    record = json.loads(request.data)
    output = model.predict_wf_wl(record['nitawade_wl'], record['nitawade_wf'], record['balinge_wl'], record['balinge_wf'])

    #insert query of predicted Data
    s = "INSERT INTO public.predicted_data(waterflow, waterlevel, station_id) VALUES (%s, %s, %s);"
    
    #inserting data of Shingnapur
    data = (output['shingnapur_wf'], output['shingnapur_wl'], 3)
    cur.execute(s, data)
    conn.commit()
    cur.execute(up, data)
    conn.commit()
    
    #inserting data of Ichalkaranji
    data = (output['ichalkaranji_wf'], output['ichalkaranji_wl'], 5)
    cur.execute(s, data)
    conn.commit()
    cur.execute(up, data)
    conn.commit()

    #inserting data of rajaram_bandhara
    data = (output['rajaram_bandhara_wf'], output['rajaram_bandhara_wl'], 4)
    cur.execute(s, data)
    conn.commit()
    cur.execute(up, data)
    conn.commit()
    return jsonify(output)

@app.route('/station_details', methods=['GET'])
def station_details():
    cur = conn.cursor()
    s = "select * from station_details;"
    cur.execute(s)
    output1 = cur.fetchall()
    output=[]
    for i in output1:
        output2 = {
            "id": i[0],
            "name": i[1],
            "latitude": i[2],
            "longitude": i[3],
            "district": i[4],
            "taluka": i[5],
            "waterflow": i[6],
            "waterlevel": i[7],
            "predicted_wf": i[8],
            "predicted_wl": i[9],
            "alert": i[10],
            "user_id": i[11],
            "time_stamp": i[12],
        }
        output.append(output2)
    conn.commit()
    return jsonify(output)

@app.route('/stored_data', methods=['GET'])
def stored_data():
    cur = conn.cursor()
    s = "SELECT name, stored_data.water_flow, stored_data.water_level, stored_data.time_stamp from stored_data INNER JOIN station_details as sd ON stored_data.station_id = sd.id;"
    cur.execute(s)
    output = cur.fetchall()
    conn.commit()
    return jsonify(output)

@app.route('/predicted_data', methods=['GET'])
def predicted_data():
    cur = conn.cursor()
    s = "SELECT name, predicted_data.waterflow, predicted_data.waterlevel, predicted_data.time_stamp from predicted_data INNER JOIN station_details as sd ON predicted_data.station_id = sd.id;"
    cur.execute(s)
    output = cur.fetchall()
    conn.commit()
    return jsonify(output)

# app.run(debug=True)