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


@app.route('/hbnb')
def hbnb_route():
    """HBNB route"""

    def sort_by_name(obj):
        return obj.name

    states = list(storage.all('State').values())
    amenities = list(storage.all('Amenity').values())
    places = list(storage.all('Place').values())

    return render_template('100-hbnb.html',
                           states=sorted(states, key=sort_by_name),
                           amenities=sorted(amenities, key=sort_by_name),
                           places=sorted(places, key=sort_by_name))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
