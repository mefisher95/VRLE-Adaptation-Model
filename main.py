from flask import Flask, render_template, request, url_for, redirect, session
import re
import webbrowser
import time
import random
from Anomaly import *
from Decision_module import *
from Queue import Priority_Queue
app =Flask(__name__)
app.secret_key = 'testing'

def validate():
    dir_files = os.listdir(os.getcwd() + '/csv')

    if ('Decision_units.csv' not in os.listdir(os.getcwd() + '/csv') or
        'solutions.csv' not in os.listdir(os.getcwd() + '/csv')):
       print('initializing') 
       Decision_module(build=True)


@app.route('/')
def main():
    return redirect(url_for('monitor', ready=True))

@app.route('/home/<ready>', methods=['GET', 'POST'])
def monitor(ready = True):
    ready = eval(ready)
    queue = Priority_Queue()
    adaptation_model = Decision_module()
    anomaly = None

    if ready is False:
        anomaly = Anomaly()
        anomaly.read()
        queue.read(Solution)
        if request.method == 'POST':
            delta_cs = request.form['delta_cs']
            print(delta_cs)
            if 'good_solution' in request.form or 'bad_solution' in request.form:
                 # edge case if all solutions have been tried
                if queue.len() < 1: return redirect(url_for('monitor', ready=True))

                if 'bad_solution' in request.form:
                    filename = 'csv/training_manuel.csv'
                    serial_list = [(anomaly.serialize(), queue.head().serialize(), 0, delta_cs)]
                    adaptation_model.organic_teaching(anomaly, queue.head(), 0)
                    write(filename, serial_list, 'a')
                    queue.pop()
                    queue.write()
                    anomaly.write()
                    return redirect(url_for('monitor', ready=False))
                elif 'good_solution' in request.form:
                    filename = 'csv/training_manuel.csv'
                    serial_list = [(anomaly.serialize(), queue.head().serialize(), 1, delta_cs)]
                    adaptation_model.organic_teaching(anomaly, queue.head(), 1)
                    write(filename, serial_list, 'a')
                    write_adaptations(queue.head())
                    return redirect(url_for('monitor', ready=True))
    else:
        if request.method == 'POST':
            if 'get_anomaly' in request.form:
                anomaly = get_sample_anomaly(1)[0]
                anomaly.write()
                write_csv_log([anomaly])
                # write_adaptations(adaptation_model.process_anomaly([anomaly]))
                

                queue = Priority_Queue()
                queue.list_to_queue(adaptation_model.process_anomaly([anomaly]))
                print(queue)
                queue.write()
                return redirect(url_for('monitor', ready=False))
    
    return render_template('monitor.html', active_queue=queue.queue_to_list(), 
                            active_anomaly=anomaly, ready=ready,
                            anomalies = read_csv_log(),
                            model = adaptation_model,
                            solutions = read_adaptations())

if __name__ == '__main__':
   
    validate()
    app.run(debug=False)