from flask import Flask, render_template, request, url_for, redirect, jsonify
import re
import webbrowser
import time
import random
from Knowledge_base import *
from Adaptation_framework import *
app =Flask(__name__)

@app.route('/')
def main():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/fields')
def fields():
    return render_template('fields.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        string = request.form['string_input']
        delim = request.form['delim_input']

        parsed_string = re.split("[%s]+" % delim, string)
        if "" in parsed_string:
            parsed_string.remove("")

        return render_template('data.html', parsed_string=parsed_string)
    return render_template('data.html', parsed_string=None)

@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    anomalies = []
    solutions = []
    adaptation_model = Adaptation_framework(solution_num=10)
    if request.method == 'POST':
        anomaly = get_sample_anomaly(1)
        anomalies.append(anomaly[0])
        solutions.append(adaptation_model.process_anomaly(anomaly))
        return render_template("Monitor.html", anomalies = anomalies, model = adaptation_model, solutions = solutions)
    return render_template("Monitor.html", anomalies = anomalies, model = adaptation_model, solutions = solutions)

@app.route('/_stuff', methods=['GET'])
def stuff():
    return jsonify(result=random.randint(0, 20))

@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(debug=True)