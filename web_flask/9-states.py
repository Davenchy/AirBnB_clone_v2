#!/usr/bin/python3
"""Host database states sample data using template"""

from models import storage
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(_):
    """Close db session after each request"""
    if storage is not None:
        storage.close()


@app.route('/states')
def states_route():
    """All states route"""
    states = storage.all('State').values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>')
def state_id_route(id):
    """State info by id route"""
    states = storage.all('State').values()
    for state in states:
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html', notFound=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
