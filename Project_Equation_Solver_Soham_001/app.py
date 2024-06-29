from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    eq_type = data['type']
    
    if eq_type == 'quadratic':
        a = float(data['a'])
        b = float(data['b'])
        c = float(data['c'])
        D = (b**2) - (4*a*c)
        if D >= 0:
            x1 = (-b + (D**0.5)) / (2*a)
            x2 = (-b - (D**0.5)) / (2*a)
            roots = [x1, x2]
        else:
            roots = ["Complex roots"]
        
        # Plot the quadratic equation
        x = np.linspace(-10, 10, 400)
        y = a*x**2 + b*x + c
        plt.figure()
        plt.plot(x, y, label=f'{a}x^2 + {b}x + {c}')
        plt.axhline(0, color='black',linewidth=0.5)
        plt.axvline(0, color='black',linewidth=0.5)
        plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        plt.legend()
        
    elif eq_type == 'cubic':
        a = float(data['a'])
        b = float(data['b'])
        c = float(data['c'])
        d = float(data['d'])
        roots = solve_cubic(a, b, c, d)
        
        # Plot the cubic equation
        x = np.linspace(-10, 10, 400)
        y = a*x**3 + b*x**2 + c*x + d
        plt.figure()
        plt.plot(x, y, label=f'{a}x^3 + {b}x^2 + {c}x + {d}')
        plt.axhline(0, color='black',linewidth=0.5)
        plt.axvline(0, color='black',linewidth=0.5)
        plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        plt.legend()

    # Save plot to a string in base64 format
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return jsonify(roots=roots, plot_url=plot_url)

def solve_cubic(a, b, c, d):
    # Find the roots of the cubic equation ax^3 + bx^2 + cx + d = 0
    p = -b/(3*a)
    q = p**3 + (b*c - 3*a*d)/(6*a**2)
    r = c/(3*a)
    discriminant = q**2 + (r - p**2)**3

    if discriminant > 0:
        S = np.cbrt(q + np.sqrt(discriminant))
        T = np.cbrt(q - np.sqrt(discriminant))
        roots = [S + T + p]
    elif discriminant == 0:
        S = np.cbrt(q)
        roots = [2*S + p, -S + p]
    else:
        rho = np.sqrt(-(r - p**2)**3)
        theta = np.arccos(q/rho)
        rho = np.cbrt(rho)
        roots = [
            2*rho*np.cos(theta/3) + p,
            2*rho*np.cos((theta + 2*np.pi)/3) + p,
            2*rho*np.cos((theta + 4*np.pi)/3) + p
        ]
    
    return roots

if __name__ == '__main__':
    app.run(debug=True)
