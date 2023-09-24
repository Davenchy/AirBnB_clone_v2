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


@app.route('/hbnb_filters')
def hbnb_filters_route():
    """HBNB filters route"""

    def sort_by_name(obj):
        return obj.name

    states = list(storage.all('State').values())
    amenities = list(storage.all('Amenity').values())

    return render_template('10-hbnb_filters.html',
                           states=sorted(states, key=sort_by_name),
                           amenities=sorted(amenities, key=sort_by_name))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
