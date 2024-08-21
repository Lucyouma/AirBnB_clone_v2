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


@app.route('/cities_by_states', strict_slashes=False)
def list_of_cities():
    """
    renders html with cities ordered by states
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda k: k.name)
    state_list = []
    for state in sorted_states:
        state_list.append([state, sorted(state.cities, key=lambda j: j.name)])
    return render_template('8-cities_by_states.html',
                           states=state_list,
                           h_1="States")
if __name__ == "__main__":
    """
    Main
    """
    app.run(host='0.0.0.0', port=5000)
