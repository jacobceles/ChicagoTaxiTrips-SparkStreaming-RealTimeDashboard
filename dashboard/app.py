from flask import Flask, jsonify, request
from flask import render_template
import ast

app = Flask(__name__)

labels0 = []
values0 = []
labels1 = []
values1 = []
labels2 = []
values2_1 = []
values2_2 = []
labels3 = []
values3 = []
labels4 = []
values4 = []
labels5 = []
values5 = []


@app.route("/")
def get_chart_page():
    global labels0, values0, labels1, values1, labels2, values2_1, values2_2, \
        labels3, values3, labels4, values4, labels5, values5
    labels0 = []
    values0 = []
    labels1 = []
    values1 = []
    labels2 = []
    values2_1 = []
    values2_2 = []
    labels3 = []
    values3 = []
    labels4 = []
    values4 = []
    labels5 = []
    values5 = []
    return render_template('index.html',
                           labels0=labels0, values0=values0,
                           labels1=labels1, values1=values1,
                           labels2=labels2,
                           values2_1=values2_1, values2_2=values2_2,
                           labels3=labels3, values3=values3,
                           labels4=labels4, values4=values4,
                           labels5=labels5, values5=values5)


@app.route('/refreshData')
def refresh_graph_data():
    global labels0, values0, labels1, values1, labels2, values2_1, values2_2, \
        labels3, values3, labels4, values4, labels5, values5
    print("Labels0 now: " + str(labels0))
    print("Values0 now: " + str(values0))
    print("Labels1 now: " + str(labels1))
    print("Values1 now: " + str(values1))
    print("Labels2 now: " + str(labels2))
    print("Values2_1 now: " + str(values2_1))
    print("Values2_2 now: " + str(values2_2))
    print("Labels3 now: " + str(labels3))
    print("Values3 now: " + str(values3))
    print("Labels4 now: " + str(labels4))
    print("Values4 now: " + str(values4))
    print("Labels5 now: " + str(labels5))
    print("Values5 now: " + str(values5))
    return jsonify(labels0=labels0, values0=values0,
                   labels1=labels1, values1=values1,
                   labels2=labels2,
                   values2_1=values2_1, values2_2=values2_2,
                   labels3=labels3, values3=values3,
                   labels4=labels4, values4=values4,
                   labels5=labels5, values5=values5)


@app.route('/updateData', methods=['POST'])
def update_data():
    global labels0, values0, labels1, values1, labels2, values2_1, values2_2, \
        labels3, values3, labels4, values4, labels5, values5
    if 'values0' in str(request.form):
        labels0 = ast.literal_eval(request.form['labels0'])
        values0 = ast.literal_eval(request.form['values0'])
    if 'values1' in str(request.form):
        labels1 = ast.literal_eval(request.form['labels1'])
        values1 = ast.literal_eval(request.form['values1'])
    elif 'values2_1' in str(request.form):
        labels2 = ast.literal_eval(request.form['labels2'])
        values2_1 = ast.literal_eval(request.form['values2_1'])
    elif 'values2_2' in str(request.form):
        labels2 = ast.literal_eval(request.form['labels2'])
        values2_2 = ast.literal_eval(request.form['values2_2'])
    elif 'values3' in str(request.form):
        labels3 = ast.literal_eval(request.form['labels3'])
        values3 = ast.literal_eval(request.form['values3'])
    elif 'values4' in str(request.form):
        labels4 = ast.literal_eval(request.form['labels4'])
        values4 = ast.literal_eval(request.form['values4'])
    elif 'values5' in str(request.form):
        labels5 = ast.literal_eval(request.form['labels5'])
        values5 = ast.literal_eval(request.form['values5'])
    else:
        return "error", 400
    print("Labels0 Received: " + str(labels0))
    print("Values0 Received: " + str(values0))
    print("Labels1 Received: " + str(labels1))
    print("Values1 Received: " + str(values1))
    print("Labels2 Received: " + str(labels2))
    print("Values2_1 Received: " + str(values2_1))
    print("Values2_2 Received: " + str(values2_2))
    print("Labels3 Received: " + str(labels3))
    print("Values3 Received: " + str(values3))
    print("Labels4 Received: " + str(labels4))
    print("Values4 Received: " + str(values4))
    print("Labels5 Received: " + str(labels5))
    print("Values5 Received: " + str(values5))
    return "success", 201


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
