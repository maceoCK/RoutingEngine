import json
from datetime import datetime, timedelta
import random
import numpy as np

with open("fakeLocationData.json", "w") as f:
    data = {"locations": []}

    for i in range(100):
        latitude = random.uniform(37.224711, 37.242507)
        longitude = random.uniform(-80.456073, -80.402488)
        rand_min = random.randint(0, 59)
        request_time = (datetime.now() + timedelta(minutes=rand_min)).strftime("%Y-%m-%dT%H:%M:%S")
        party_size = max(1, int(np.random.normal(3, 2)))  # Ensure party size is a positive integer

        location = {
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "requestTime": request_time,
            "partySize": party_size
        }

        data["locations"].append(location)

    f.write(json.dumps(data, indent=4))
