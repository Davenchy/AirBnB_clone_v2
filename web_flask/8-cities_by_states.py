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


@app.route('/states_list')
def states_list_route():
    """States list route"""
    states = storage.all('State').values()
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states')
def cities_by_states_route():
    """Cities by states route"""
    states = storage.all('State').values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
