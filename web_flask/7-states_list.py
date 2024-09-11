#!/usr/bin/python3
"""
endpoint to render template with states
"""
from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """
    closes Sqlalachemy session
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    renders html page with states
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda j: j.name)
    return render_template('7-states_list.html', states=sorted_states)


if __name__ == "__main__":
    """
    Main
    """
    app.run(host='0.0.0.0', port=5000)
