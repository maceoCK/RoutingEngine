from flask import Flask, request, jsonify
from geopy import Nominatim
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

addresses_queue = []


def get_coordinates(address):
    geolocator = Nominatim(user_agent="app")
    location = geolocator.geocode(address)
    print(location, str(location.latitude), str(location.longitude))
    if location:
        return (location.latitude, location.longitude)
    else:
        return None


@app.route("/add_address", methods=["POST"])
def add_address():
    data = request.json
    address = data["address"]
    coords = get_coordinates(address)
    addresses_queue.append(coords)
    return (
        jsonify(
            {
                "message": "Address added successfully",
                "queue_length": len(addresses_queue),
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
