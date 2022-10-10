DATABASE = {
    "animals": [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 1,
            "status": "Admitted"
        },
        {
            "id": 2,
            "name": "Roman",
            "species": "Dog",
            "locationId": 1,
            "customerId": 1,
            "status": "Admitted"
        },
        {
            "id": 3,
            "name": "Blue",
            "species": "Cat",
            "locationId": 2,
            "customerId": 1,
            "status": "Admitted"
        }
    ],
    "customers": [
        {
            "id": 1,
            "fullName": "Ryan Tanay",
            "email": "ryan.tanay@gmail.com"
        }
    ],
    "employees": [
        {
            "id": 1,
            "name": "Jenna Solis"
        }
    ],
    "locations": [
        {
            "id": 1,
            "name": "Nashville North",
            "address": "8422 Johnson Pike"
        },
        {
            "id": 2,
            "name": "Nashville South",
            "address": "209 Emory Drive"
        }
    ]
 }

def expand(resource, key, data):
    matching_data = retrieve(resource, data[key])
    data[key[:-2]] = matching_data
    del data[key]

def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]

def retrieve(resource, id):
    """For GET requests to a single resource"""
    requested_data = None

    for data in DATABASE[resource]:
        if data["id"] == id:
            requested_data = data

            if resource == "animals":
                expand("locations", "locationId", requested_data)
                expand("customers", "customerId", requested_data)

    return requested_data

def create(resource, new_data):
    """For POST requests to a collection"""
    max_id = DATABASE[resource][-1]["id"]
    new_id = max_id + 1
    new_data["id"] = new_id
    DATABASE[resource].append(new_data)
    return new_data

def update(resource, id, edited_data):
    """For PUT requests to a single resource"""
    for index, data in enumerate(DATABASE[resource]):
        if data["id"] == id:
            DATABASE[resource][index] = edited_data
            break

def delete(resource, id):
    """For DELETE requests to a single resource"""
    data_index = -1

    for index, data in enumerate(DATABASE[resource]):
        if data["id"] == id:
            data_index = index

        if data_index >= 0:
            DATABASE[resource].pop(data_index)
    