# encoding: utf-8
import json
from click import password_option
from flask import Flask, request, jsonify, send_from_directory
from numpy import outer
import model as model 
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

conn = psycopg2.connect(dbname="d4bi30pog6cpff", user="lktmtqhlqduqwo", password="e99d63085169e1aa483d4ea42af9d168953c669eb06feea68cff02b06f0bf310", host="ec2-23-20-73-25.compute-1.amazonaws.com")

@app.route('/', methods=['GET'])
def hiii():
    return "Hello"

@app.route('/favicon.ico', methods=['GET']) 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/predict', methods=['POST'])
def update_record():    
    record = json.loads(request.data)
    cur = conn.cursor()
    #insert query of stored Data
    s = "INSERT INTO public.stored_data(water_flow, water_level, station_id) VALUES (%s, %s, %s);"
    ur = "UPDATE station_details SET waterflow = %s, waterlevel = %s, time_stamp=now() where id = %s;"
    up = "UPDATE station_details SET predicted_wf = %s, predicted_wl = %s where id = %s;"
    
    #inserting data of Nitawade
    data = (record['nitawade_wf'], record['nitawade_wl'], 6)
    cur.execute(s, data)
    cur.execute(ur, data)
    conn.commit()

    #Updating WF and WL Data of Nitawade

    #inserting data of Balinge
    data = (record['balinge_wf'], record['balinge_wl'], 7)
    cur.execute(s, data)
    cur.execute(ur, data)
    conn.commit()

    record = json.loads(request.data)
    output = model.predict_wf_wl(record['nitawade_wl'], record['nitawade_wf'], record['balinge_wl'], record['balinge_wf'])

    #insert query of predicted Data
    s = "INSERT INTO public.predicted_data(waterflow, waterlevel, station_id) VALUES (%s, %s, %s);"
    
    #inserting data of Shingnapur
    data = (output['shingnapur_wf'], output['shingnapur_wl'], 8)
    cur.execute(s, data)
    cur.execute(up, data)
    conn.commit()
    
    #inserting data of Ichalkaranji
    data = (output['ichalkaranji_wf'], output['ichalkaranji_wl'], 10)
    cur.execute(s, data)
    cur.execute(up, data)
    conn.commit()

    #inserting data of rajaram_bandhara
    data = (output['rajaram_bandhara_wf'], output['rajaram_bandhara_wl'], 9)
    cur.execute(s, data)
    cur.execute(up, data)
    conn.commit()
    return jsonify(output)

@app.route('/station_details', methods=['GET'])
def station_details():
    cur = conn.cursor()
    s = "select * from station_details;"
    cur.execute(s)
    output = cur.fetchall()
    conn.commit()
    return jsonify(output)

@app.route('/stored_data', methods=['GET'])
def stored_data():
    cur = conn.cursor()
    s = "SELECT name, stored_data.water_flow, stored_data.water_level, time_stamp from stored_data INNER JOIN station_details as sd ON stored_data.station_id = sd.id;"
    cur.execute(s)
    output = cur.fetchall()
    conn.commit()
    return jsonify(output)

@app.route('/predicted_data', methods=['GET'])
def predicted_data():
    cur = conn.cursor()
    s = "SELECT name, predicted_data.waterflow, predicted_data.waterlevel, time_stamp from predicted_data INNER JOIN station_details as sd ON predicted_data.station_id = sd.id;"
    cur.execute(s)
    output = cur.fetchall()
    conn.commit()
    return jsonify(output)

app.run(debug=True)