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


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def state_param(id=""):
    """
    renders html with cities ordered by states
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda k: k.name)
    found = 0
    state = ""
    cities = []

    for k in states:
        if id == k.id:
            state = k
            found = 1
            break
    if found:
        sorted_states = sorted(state.cities, key=lambda j: j.name)
        state = sorted_states.name
    if id and not found:
        found = 2

    return render_template('9-states.html',
                           state=state,
                           array=states,
                           found=found)


if __name__ == "__main__":
    """
    Main
    """
    app.run(host='0.0.0.0', port=5000)
