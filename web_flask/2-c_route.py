#!/usr/bin/python3
"""
Start Web application; endpoint
returns 'C is Fun'
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    prints message with route
    '/'
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Prints"HBNB" on endpoint
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_fun(text):
    """
    prints message with input text parameter
    """
    return "C " + text.replace('_', ' ')


if __name__ == "__main__":
    """
    main
    """
    app.run(host='0.0.0.0', port=5000)
