import math
import matplotlib.pyplot as plt
from flask import Flask, redirect, url_for, request, render_template
import io
import base64

app = Flask(__name__)

def create_graph(A, B, C, x0, v0):
    l1 = -B/(2*A) + pow(abs(B**2 - 4*A*C), 0.5)/(2*A) 
    l2 = -B/(2*A) - pow(abs(B**2 - 4*A*C), 0.5)/(2*A)
    if l1 != l2:
        D1 = (v0 - l2*x0) / (l1 - l2)
        D2 = (v0 - l1*x0) / (l2 - l1)
    alp = -B/(2*A) 
    bita = pow(abs(B**2 - 4*A*C), 0.5)/(2*A)
    t = [i / 10 for i in range(51)]

    if (B**2 - 4*A*C) > 0:
        sol = []  # it is an accumulator to store the solution of overdamping
        for i in range(len(t)):
            x = D1 * math.exp(l1*t[i]) + D2 * math.exp(l2*t[i])
            sol.append(x)
        plt.plot(t, sol)
        plt.title("Over Damping")
    elif (B**2 - 4*A*C) == 0:
        sol = []  # it is an accumulator to store the solution of critical damping
        for i in range(len(t)):
            x = (x0 + (v0 - alp*x0)) * math.exp(alp*t[i])
            sol.append(x)
        plt.plot(t, sol)
        plt.title("Critical Damping")
    else:
        sol = []  # it is an accumulator to store the solution of underdamped
        for i in range(len(t)):
            x = math.exp(-alp*t[i]) * ((x0 * math.cos(bita*t[i]) + (v0 + alp*x0) * math.sin(bita*t[i])) / bita)
            sol.append(x)
        plt.plot(t, sol)
        plt.title("Underdamped")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the buffer to base64 string
    graph = base64.b64encode(buffer.read()).decode('utf-8')
    return graph

@app.route("/graph/<float:A>/<float:B>/<float:C>/<float:x0>/<float:v0>")
def graph(A, B, C, x0, v0):
    # Convert the parameters to float before passing them to create_graph
    graph_data = create_graph(float(A), float(B), float(C), float(x0), float(v0))
    return render_template('graph.html', graph_data=graph_data)

@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_A = request.form['A']
        user_B = request.form['B']
        user_C = request.form['C']
        user_x0 = request.form['x0']
        user_v0 = request.form['v0']
        return redirect(url_for('graph', A=user_A, B=user_B, C=user_C, x0=user_x0, v0=user_v0))
    else:
        user_A = request.args.get('A')
        user_B = request.args.get('B')
        user_C = request.args.get('C')
        user_x0 = request.args.get('x0')
        user_v0 = request.args.get('v0')
        return render_template("graph.html")






























