from flask import Flask, render_template, request, url_for, redirect, jsonify
import re
import webbrowser
import time
import random
from Anomaly import *
from Adaptation_framework import *
app =Flask(__name__)

def validate():
    dir_files = os.listdir(os.getcwd() + '/csv')

    if ('decision_modules.csv' not in os.listdir(os.getcwd() + '/csv') or
        'solutions.csv' not in os.listdir(os.getcwd() + '/csv')):
       print('initializing') 
       Adaptation_framework(build=True)


@app.route('/')
def main():
    return redirect(url_for('monitor'))

@app.route('/home', methods=['GET', 'POST'])
def monitor():
    adaptation_model = Adaptation_framework(build=False)
    
    if request.method == 'POST':
        if 'get_anomaly' in request.form:
            anomaly = get_sample_anomaly(1)
            write_csv_log(anomaly)
            write_adaptations(adaptation_model.process_anomaly(anomaly))
        elif 'gen_model' in request.form:
             adaptation_model = Adaptation_framework(build=True)
        return render_template("Monitor.html", anomalies = read_csv_log(), model = adaptation_model, solutions = read_adaptations())
    return render_template("Monitor.html", anomalies = read_csv_log(), model = adaptation_model, solutions = read_adaptations())

if __name__ == '__main__':
    validate()
    app.run(debug=False)