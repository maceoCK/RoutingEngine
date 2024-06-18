import datetime
from flask import Flask, request, jsonify
from geopy import Nominatim
from flask_cors import CORS
from example import collection

app = Flask(__name__)
CORS(app)

addresses_queue = []

geolocator = Nominatim(user_agent="app", timeout=10)


def get_coordinates(address):
    location = geolocator.geocode(address)
    # print(location, str(location.latitude), str(location.longitude))
    if location:
        return (location.latitude, location.longitude)
    else:
        return None


@app.route("/add_address", methods=["POST"])
def add_address():
    data = request.json

    address = get_coordinates(data["address"])
    while address != None:
        party_size = int(data["partySize"])
        currentTime = str(datetime.datetime.now())
        location = str(geolocator.geocode(data["address"]))
        document = {
            "coordinates": {"latitude": address[0], "longitude": address[1]},
            "requestTime": currentTime,
            "partySize": party_size,
        }
        collection.insert_one(document)
        # addresses_queue.append(address)
        return (
            jsonify({"message": "Submitted!"}),
            200,
        )
    return (
        jsonify({"message": "Address Not Found!"}),
        200,
    )

@app.route("/verify_address", methods=["POST"])
def verify_address():
    data = request.json

    address = get_coordinates(data["address"])
    while address != None:
        party_size = int(data["partySize"])
        currentTime = str(datetime.datetime.now())
        location = str(geolocator.geocode(data["address"]))
        document = {
            "coordinates": {"latitude": address[0], "longitude": address[1]},
            "requestTime": currentTime,
            "partySize": party_size,
        }
        # addresses_queue.append(address)
        return (
            jsonify({"message": location}),
            200,
        )
    return (
        jsonify({"message": "Address Not Found!"}),
        200,
    )

if __name__ == "__main__":
    app.run(debug=True)
